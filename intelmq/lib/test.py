# -*- coding: utf-8 -*-
"""
Utilities for testing intelmq bots.

The BotTestCase can be used as base class for unittests on bots. It includes
some basic generic tests (logged errors, correct pipeline setup).
"""
import copy
import io
import json
import logging
import os
import re
import unittest
import unittest.mock as mock
from itertools import chain

import intelmq.lib.message as message
import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
import pkg_resources
import redis
from intelmq import CONFIG_DIR, PIPELINE_CONF_FILE, RUNTIME_CONF_FILE

__all__ = ['BotTestCase']

BOT_CONFIG = {"http_proxy": None,
              "https_proxy": None,
              "broker": "pythonlist",
              "rate_limit": 0,
              "retry_delay": 0,
              "error_retry_delay": 0,
              "error_max_retries": 0,
              "redis_cache_host": "localhost",
              "redis_cache_port": 6379,
              "redis_cache_db": 4,
              "redis_cache_ttl": 10,
              "redis_cache_password": os.environ.get('INTELMQ_TEST_REDIS_PASSWORD'),
              "testing": True,
              }


def mocked_config(bot_id='test-bot', src_name='', dst_names=(), sysconfig={}, group=None, module=None):
    def mocked(conf_file):
        if conf_file == PIPELINE_CONF_FILE:
            return {bot_id: {"source-queue": src_name,
                             "destination-queues": dst_names},
                    }
        elif conf_file == RUNTIME_CONF_FILE:
            conf = BOT_CONFIG.copy()
            conf.update(sysconfig)
            return {bot_id: {'description': 'Instance of a bot for automated unit tests.',
                             'group': group,
                             'module': module,
                             'name': 'Test Bot',
                             'parameters': conf,
                             }}
        elif conf_file.startswith(CONFIG_DIR):
            confname = os.path.join('etc/', os.path.split(conf_file)[-1])
            fname = pkg_resources.resource_filename('intelmq',
                                                    confname)
            with open(fname, 'rt') as fpconfig:
                return json.load(fpconfig)
        else:
            return utils.load_configuration(conf_file)

    return mocked


def mocked_logger(logger):
    def log(name, log_path=None, log_level=None, stream=None, syslog=None):
        # Return a copy as the bot may modify the logger and we should always return the intial logger
        logger_new = copy.copy(logger)
        logger_new.setLevel(log_level)
        return logger_new

    return log


def skip_database():
    return unittest.skipUnless(os.environ.get('INTELMQ_TEST_DATABASES'),
                               'Skipping database tests.')


def skip_internet():
    return unittest.skipIf(os.environ.get('INTELMQ_SKIP_INTERNET'),
                           'Skipping without internet connection.')


def skip_redis():
    return unittest.skipIf(os.environ.get('INTELMQ_SKIP_REDIS'),
                           'Skipping without running redis.')


def skip_local_web():
    return unittest.skipUnless(os.environ.get('INTELMQ_TEST_LOCAL_WEB'),
                               'Skipping local web tests.')


def skip_exotic():
    return unittest.skipUnless(os.environ.get('INTELMQ_TEST_EXOTIC'),
                               'Skipping tests requiring exotic libs.')


class BotTestCase(object):
    """
    Provides common tests and assert methods for bot testing.
    """

    bot_types = {'collector': 'CollectorBot',
                 'parser': 'ParserBot',
                 'expert': 'ExpertBot',
                 'output': 'OutputBot',
                 }

    @classmethod
    def setUpClass(cls):
        """
        Set default values and save original functions.
        """
        cls.bot_id = 'test-bot'
        cls.bot_name = None
        cls.bot = None
        cls.bot_reference = None
        cls.bot_type = None
        cls.default_input_message = ''
        cls.input_message = None
        cls.loglines = []
        cls.loglines_buffer = ''
        cls.log_stream = None
        cls.maxDiff = None  # For unittest module, prints long diffs
        cls.pipe = None
        cls.sysconfig = {}
        cls.use_cache = False
        cls.allowed_warning_count = 0
        cls.allowed_error_count = 0  # allows dumping of some lines

        cls.set_bot()

        cls.bot_name = cls.bot_reference.__name__
        if cls.bot_type is None:
            for type_name, type_match in cls.bot_types.items():
                if cls.bot_name.endswith(type_match):
                    cls.bot_type = type_name
                    break
        if cls.bot_type == 'parser' and cls.default_input_message == '':
            cls.default_input_message = {'__type': 'Report',
                                         'raw': 'Cg==',
                                         'feed.name': 'Test Feed',
                                         'time.observation': '2016-01-01T00:00:00+00:00'}
        elif cls.bot_type != 'collector' and cls.default_input_message == '':
            cls.default_input_message = {'__type': 'Event'}
        if type(cls.default_input_message) is dict:
            cls.default_input_message = \
                utils.decode(json.dumps(cls.default_input_message))

        if cls.use_cache and not os.environ.get('INTELMQ_SKIP_REDIS'):
            password = os.environ.get('INTELMQ_TEST_REDIS_PASSWORD') or \
                (BOT_CONFIG['redis_cache_password'] if 'redis_cache_password' in BOT_CONFIG else None)
            cls.cache = redis.Redis(host=BOT_CONFIG['redis_cache_host'],
                                    port=BOT_CONFIG['redis_cache_port'],
                                    db=BOT_CONFIG['redis_cache_db'],
                                    socket_timeout=BOT_CONFIG['redis_cache_ttl'],
                                    password=password,
                                    )

    harmonization = utils.load_configuration(pkg_resources.resource_filename('intelmq',
                                                                             'etc/harmonization.conf'))

    def new_report(self, auto=False, examples=False):
        return message.Report(harmonization=self.harmonization, auto=auto)

    def new_event(self):
        return message.Event(harmonization=self.harmonization)

    def prepare_bot(self, parameters={}):
        """Reconfigures the bot with the changed attributes"""

        self.log_stream = io.StringIO()

        src_name = "{}-input".format(self.bot_id)
        dst_names = {"_default": "{}-output".format(self.bot_id),
                     "other-way": "{}-other-output".format(self.bot_id),
                     "two-way": ["{}-way1-output".format(self.bot_id), "{}-way2-output".format(self.bot_id)]}

        config = self.sysconfig.copy()
        config.update(parameters)
        self.mocked_config = mocked_config(self.bot_id,
                                           src_name,
                                           dst_names,
                                           sysconfig=config,
                                           group=self.bot_type.title(),
                                           module=self.bot_reference.__module__,
                                           )

        logger = logging.getLogger(self.bot_id)
        logger.setLevel("INFO")
        console_formatter = logging.Formatter(utils.LOG_FORMAT)
        console_handler = logging.StreamHandler(self.log_stream)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        self.mocked_log = mocked_logger(logger)
        logging.captureWarnings(True)
        warnings_logger = logging.getLogger("py.warnings")
        warnings_logger.addHandler(console_handler)

        class Parameters(object):
            source_queue = src_name
            destination_queues = dst_names

        parameters = Parameters()
        self.pipe = pipeline.Pythonlist(parameters)
        self.pipe.set_queues(parameters.source_queue, "source")
        self.pipe.set_queues(parameters.destination_queues, "destination")

        with mock.patch('intelmq.lib.utils.load_configuration',
                        new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.mocked_log):
                self.bot = self.bot_reference(self.bot_id)
        if self.input_message is not None:
            if type(self.input_message) is not list:
                self.input_message = [self.input_message]
            self.input_queue = []
            for msg in self.input_message:
                if type(msg) is dict:
                    self.input_queue.append(json.dumps(msg))
                elif issubclass(type(msg), message.Message):
                    self.input_queue.append(msg.serialize())
                else:
                    self.input_queue.append(msg)
            self.input_message = None
        else:
            if self.default_input_message:  # None for collectors
                self.input_queue = [self.default_input_message]

    def run_bot(self, iterations: int = 1, error_on_pipeline: bool = False, prepare=True):
        """
        Call this method for actually doing a test run for the specified bot.

        Parameters:
            iterations: Bot instance will be run the given times, defaults to 1.
        """
        if prepare:
            self.prepare_bot()
        with mock.patch('intelmq.lib.utils.load_configuration',
                        new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.mocked_log):
                for run in range(iterations):
                    self.bot.start(error_on_pipeline=error_on_pipeline,
                                   source_pipeline=self.pipe,
                                   destination_pipeline=self.pipe)
        self.loglines_buffer = self.log_stream.getvalue()
        self.loglines = self.loglines_buffer.splitlines()

        """ Test if all pipes are created with correct names. """
        pipenames = ["{}-input", "{}-input-internal", "{}-output", "{}-other-output", "{}-way1-output", "{}-way2-output"]
        self.assertSetEqual({x.format(self.bot_id) for x in pipenames},
                            set(self.pipe.state.keys()))
        """ Test if input queue is empty. """
        self.assertEqual(self.input_queue, [],
                         'Not all input messages have been processed. '
                         'You probably need to increase the number of '
                         'iterations of `run_bot`.')

        """ Test if report has required fields. """
        if self.bot_type == 'collector':
            for report_json in self.get_output_queue():
                report = message.MessageFactory.unserialize(report_json,
                                                            harmonization=self.harmonization)
                self.assertIsInstance(report, message.Report)
                self.assertIn('feed.name', report)
                self.assertIn('raw', report)
                self.assertIn('time.observation', report)

        """ Test if event has required fields. """
        if self.bot_type == 'parser':
            for event_json in self.get_output_queue():
                event = message.MessageFactory.unserialize(event_json,
                                                           harmonization=self.harmonization)
                self.assertIsInstance(event, message.Event)
                self.assertIn('classification.type', event)
                self.assertIn('raw', event)

        """ Test if bot log messages are correctly formatted. """
        self.assertLoglineMatches(0, "{} initialized with id {} and intelmq [0-9a-z.]* and python"
                                     r" [0-9a-z.]{{5,8}}\+? \([a-zA-Z0-9,:. ]+\)( \[GCC\])?"
                                     r" as process [0-9]+\."
                                     "".format(self.bot_name,
                                               self.bot_id), "INFO")
        self.assertRegexpMatchesLog("INFO - Bot is starting.")
        self.assertLoglineEqual(-1, "Bot stopped.", "INFO")
        self.assertNotRegexpMatchesLog("(ERROR.*?){%d}" % (self.allowed_error_count + 1))
        self.assertNotRegexpMatchesLog("(WARNING.*?){%d}" % (self.allowed_warning_count + 1))
        self.assertNotRegexpMatchesLog("CRITICAL")
        """ If no error happened (incl. tracebacks) we can check for formatting """
        if not self.allowed_error_count:
            for logline in self.loglines:
                fields = utils.parse_logline(logline)
                if not isinstance(fields, dict):
                    # Traceback
                    continue
                self.assertTrue(fields['message'][-1] in '.:?!',
                                msg='Logline {!r} does not end with .? or !.'
                                    ''.format(fields['message']))
                self.assertTrue(fields['message'].upper() == fields['message'].upper(),
                                msg='Logline {!r} does not begin with an upper case char.'
                                    ''.format(fields['message']))

    @classmethod
    def tearDownClass(cls):
        if cls.use_cache and not os.environ.get('INTELMQ_SKIP_REDIS'):
            cls.cache.flushdb()

    def get_input_queue(self):
        """Returns the input queue of this bot which can be filled
           with fixture data in setUp()"""
        if self.pipe:
            return self.pipe.state["%s-input" % self.bot_id]
        else:
            return []

    def set_input_queue(self, seq):
        """Setter for the input queue of this bot"""
        self.pipe.state["%s-input" % self.bot_id] = [utils.encode(text) for
                                                     text in seq]

    input_queue = property(get_input_queue, set_input_queue)

    def get_output_queue(self, path="_default"):
        """Getter for items in the output queues of this bot. Use in TestCase scenarios
            If there is multiple queues in named queue group, we return all the items chained.
        """
        return [utils.decode(text) for text in chain(*[self.pipe.state[x] for x in self.pipe.destination_queues[path]])]
        # return [utils.decode(text) for text in self.pipe.state["%s-output" % self.bot_id]]

    def test_bot_name(self):
        """
        Test if Bot has a valid name.
        Must be CamelCase and end with CollectorBot etc.
        Test class name must be Test{botclassname}
        """
        counter = 0
        for type_name, type_match in self.bot_types.items():
            try:
                self.assertRegex(self.bot_name,
                                 r'\A[a-zA-Z0-9]+{}\Z'.format(type_match))
            except AssertionError:
                counter += 1
        if counter != len(self.bot_types) - 1:
            self.fail("Bot name {!r} does not match one of {!r}"
                      "".format(self.bot_name, list(self.bot_types.values())))  # pragma: no cover

        self.assertEqual('Test{}'.format(self.bot_name),
                         self.__class__.__name__.split('_')[0])

    def assertAnyLoglineEqual(self, message: str, levelname: str = "ERROR"):
        """
        Asserts if any logline matches a specific requirement.

        Parameters:
            message: Message text which is compared
            type: Type of logline which is asserted

        Raises:
            ValueError: if logline message has not been found
        """

        self.assertIsNotNone(self.loglines)
        for logline in self.loglines:
            fields = utils.parse_logline(logline)

            if levelname == fields["log_level"] and message == fields["message"]:
                return
        else:
            raise ValueError('Logline with level {!r} and message {!r} not found'
                             ''.format(levelname, message))  # pragma: no cover

    def assertLoglineEqual(self, line_no: int, message: str, levelname: str = "ERROR"):
        """
        Asserts if a logline matches a specific requirement.

        Parameters:
            line_no: Number of the logline which is asserted
            message: Message text which is compared
            levelname: Log level of logline which is asserted
        """

        self.assertIsNotNone(self.loglines)
        logline = self.loglines[line_no]
        fields = utils.parse_logline(logline)

        self.assertEqual(self.bot_id, fields["bot_id"],
                         "bot_id %s didn't match %s"
                         "".format(self.bot_id, fields["bot_id"]))

        self.assertEqual(levelname, fields["log_level"])
        self.assertEqual(message, fields["message"])

    def assertLoglineMatches(self, line_no: int, pattern: str, levelname: str = "ERROR"):
        """
        Asserts if a logline matches a specific requirement.

        Parameters:
            line_no: Number of the logline which is asserted
            pattern: Message text which is compared
            type: Type of logline which is asserted
        """

        self.assertIsNotNone(self.loglines)
        logline = self.loglines[line_no]
        fields = utils.parse_logline(logline)

        self.assertEqual(self.bot_id, fields["bot_id"],
                         "bot_id %s didn't match %s"
                         "".format(self.bot_id, fields["bot_id"]))

        self.assertEqual(levelname, fields["log_level"])
        self.assertRegex(fields["message"], pattern)

    def assertLogMatches(self, pattern: str, levelname: str = "ERROR"):
        """
        Asserts if any logline matches a specific requirement.

        Parameters:
            pattern: Message text which is compared, regular expression.
            levelname: Log level of the logline which is asserted, upper case.
        """

        self.assertIsNotNone(self.loglines)
        for logline in self.loglines:
            fields = utils.parse_logline(logline)

            #  Exception tracebacks
            if isinstance(fields, str):
                if levelname == "ERROR" and re.match(pattern, fields):
                    break
            elif levelname == fields["log_level"] and re.match(pattern, fields["message"]):
                break
        else:
            raise ValueError('No matching logline found.')  # pragma: no cover

    def assertRegexpMatchesLog(self, pattern):
        """Asserts that pattern matches against log. """

        self.assertIsNotNone(self.loglines_buffer)
        self.assertRegex(self.loglines_buffer, pattern)

    def assertNotRegexpMatchesLog(self, pattern):
        """Asserts that pattern doesn't match against log."""

        self.assertIsNotNone(self.loglines_buffer)
        self.assertNotRegex(self.loglines_buffer, pattern)

    def assertOutputQueueLen(self, queue_len=0, path="_default"):
        """
        Asserts that the output queue has the expected length.
        """
        self.assertEqual(len(self.get_output_queue(path=path)), queue_len)

    def assertMessageEqual(self, queue_pos, expected_msg, compare_raw=True, path="_default"):
        """
        Asserts that the given expected_message is
        contained in the generated event with
        given queue position.
        """
        event = self.get_output_queue(path=path)[queue_pos]
        self.assertIsInstance(event, str)

        event_dict = json.loads(event)
        if isinstance(expected_msg, (message.Event, message.Report)):
            expected = expected_msg.to_dict(with_type=True)
        else:
            expected = expected_msg.copy()

        if not compare_raw:
            expected.pop('raw', None)
            event_dict.pop('raw', None)
        if 'time.observation' in event_dict:
            del event_dict['time.observation']
        if 'time.observation' in expected:
            del expected['time.observation']

        self.assertDictEqual(expected, event_dict)

    def tearDown(self):
        """
        Check if the bot did consume all messages.
        """
        self.assertEqual(len(self.input_queue), 0)
