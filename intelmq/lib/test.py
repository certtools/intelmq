# -*- coding: utf-8 -*-
"""
Utilities for testing intelmq bots.

TheBotTestCase can be used as base class for unittests on bots. It includes
some basic generic tests (logged errors, correct pipeline setup).
"""
import io
import json
import logging
import os

import mock
import pkg_resources

import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
from intelmq import (PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, SYSTEM_CONF_FILE,
                     CONFIG_DIR)

__all__ = ['BotTestCase']


BOT_CONFIG = {
    "logging_level": "DEBUG",
    "http_proxy": None,
    "https_proxy": None,
    "broker": "pythonlist",
    "rate_limit": 0,
    "retry_delay": 0,
    "error_retry_delay": 0,
    "error_max_retries": 0,
    "testing": True,
    "redis_cache_host": "localhost",
    "redis_cache_port": 6379,
    "redis_cache_db": 10,
    "redis_cache_ttl": 10,
}


def mocked_config(bot_id='test-bot', src_name='', dst_names=(), sysconfig={}):
    def mock(conf_file):
        if conf_file == PIPELINE_CONF_FILE:
            return {bot_id: {"source-queue": src_name,
                             "destination-queues": dst_names},
                    }
        elif conf_file == RUNTIME_CONF_FILE:
            return {bot_id: {}}
        elif conf_file == SYSTEM_CONF_FILE:
            conf = BOT_CONFIG.copy()
            conf.update(sysconfig)
            return conf
        elif conf_file.startswith(CONFIG_DIR):
            confname = os.path.join('etc/', os.path.split(conf_file)[-1])
            fname = pkg_resources.resource_filename('intelmq',
                                                    confname)
            with open(fname, 'rt') as fpconfig:
                return json.load(fpconfig)
        else:
            return utils.load_configuration(conf_file)
    return mock


with mock.patch('intelmq.lib.utils.load_configuration', new=mocked_config()):
    import intelmq.lib.message as message


def mocked_logger(logger):
    def log(name, log_path=None, log_level=None, stream=None, syslog=None):
        return logger
    return log


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
        cls.config = {}
        cls.default_input_message = ''
        cls.input_message = None
        cls.loglines = []
        cls.loglines_buffer = ''
        cls.log_stream = None
        cls.maxDiff = None  # For unittest module, prints long diffs
        cls.pipe = None
        cls.sysconfig = {}
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
                                         'time.observation': '2016-01-01T00:00'}
        if type(cls.default_input_message) is dict:
            cls.default_input_message = \
                utils.decode(json.dumps(cls.default_input_message))

    def prepare_bot(self):
        """Reconfigures the bot with the changed attributes"""

        self.log_stream = io.StringIO()

        src_name = "{}-input".format(self.bot_id)
        dst_name = "{}-output".format(self.bot_id)

        self.mocked_config = mocked_config(self.bot_id,
                                           src_name,
                                           [dst_name],
                                           sysconfig=self.sysconfig,
                                           )

        logger = logging.getLogger(self.bot_id)
        logger.setLevel("DEBUG")
        console_formatter = logging.Formatter(utils.LOG_FORMAT)
        console_handler = logging.StreamHandler(self.log_stream)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        self.mocked_log = mocked_logger(logger)

        class Parameters(object):
            source_queue = src_name
            destination_queues = [dst_name]
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
            self.input_queue = [self.default_input_message]

    def run_bot(self, iterations=1):
        """
        Call this method for actually doing a test run for the specified bot.

        Parameters
        ----------
        iterations : integer
            Bot instance will be run the given times, defaults to 1.
        """
        self.prepare_bot()
        with mock.patch('intelmq.lib.utils.load_configuration',
                        new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.mocked_log):
                for run in range(iterations):
                    self.bot.start(error_on_pipeline=False,
                                   source_pipeline=self.pipe,
                                   destination_pipeline=self.pipe)
        self.loglines_buffer = self.log_stream.getvalue()
        self.loglines = self.loglines_buffer.splitlines()

    def get_input_queue(self):
        """Returns the input queue of this bot which can be filled
           with fixture data in setUp()"""

        return self.pipe.state["%s-input" % self.bot_id]

    def set_input_queue(self, seq):
        """Setter for the input queue of this bot"""
        self.pipe.state["%s-input" % self.bot_id] = [utils.encode(text) for
                                                     text in seq]

    input_queue = property(get_input_queue, set_input_queue)

    def get_output_queue(self):
        """Getter for the input queue of this bot. Use in TestCase scenarios"""
        return [utils.decode(text) for text
                in self.pipe.state["%s-output" % self.bot_id]]

    def test_bot_start(self):
        """Tests if we can start a bot and feed data into
            it and have a reasonable output"""
        self.run_bot()

    def test_log_init(self):
        """ Test if bot logs initialized message. """
        self.run_bot()
        self.assertLoglineMatches(0, "{} initialized with id {} and version"
                                     " [0-9.]{{5}} \([a-zA-Z0-9,:. ]+\)"
                                     " as process [0-9]+\."
                                     "".format(self.bot_name,
                                               self.bot_id), "INFO")

    def test_log_starting(self):
        """ Test if bot logs starting message. """
        self.run_bot()
        self.assertRegexpMatchesLog("INFO - Bot is starting.")

    def test_log_stopped(self):
        """ Test if bot logs stopped message. """
        self.run_bot()
        self.assertLoglineEqual(-1, "Bot stopped.", "INFO")

    def test_log_end_dot(self):
        """ Test if every log lines ends with a dot. """
        for logline in self.loglines:
            fields = utils.parse_logline(logline)
            self.assertTrue(fields['message'].endswith('.'),
                            msg='Logline {} does not end with dot.'
                                ''.format(fields['message']))

    def test_log_not_error(self):
        """ Test if bot does not log errors. """
        self.run_bot()
        self.assertNotRegexpMatchesLog("(ERROR.*?){}"
                                       "".format(self.allowed_error_count))

    def test_log_not_critical(self):
        """ Test if bot does not log critical errors. """
        self.run_bot()
        self.assertNotRegexpMatchesLog("CRITICAL")

    def test_pipe_names(self):
        """ Test if all pipes are created with correct names. """
        self.run_bot()
        pipenames = ["{}-input", "{}-input-internal", "{}-output"]
        self.assertSetEqual({x.format(self.bot_id) for x in pipenames},
                            set(self.pipe.state.keys()))

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
                      "".format(self.bot_name, list(self.bot_types.values())))

        self.assertEqual('Test{}'.format(self.bot_name),
                         self.__class__.__name__)

    def test_report(self):
        """ Test if report has required fields. """
        if self.bot_type != 'collector':
            return

        self.run_bot()
        for report_json in self.get_output_queue():
            report = message.MessageFactory.unserialize(report_json)
            self.assertIsInstance(report, message.Report)
            self.assertIn('feed.name', report)
            self.assertIn('raw', report)
            self.assertIn('time.observation', report)

    def test_event(self):
        """ Test if event has required fields. """
        if self.bot_type not in ['parser', 'expert']:
            return

        self.run_bot()
        for event_json in self.get_output_queue():
            event = message.MessageFactory.unserialize(event_json)
            self.assertIsInstance(event, message.Event)
            self.assertIn('classification.type', event)
            self.assertIn('feed.name', event)
            self.assertIn('raw', event)
            self.assertIn('time.observation', event)

    def assertLoglineEqual(self, line_no, message, levelname="ERROR"):
        """Asserts if a logline matches a specific requirement.
           Args:
                line_no: Number of the logline which is asserted
                message: Message text which is compared
                type: Type of logline which is asserted"""

        self.assertIsNotNone(self.loglines)
        logline = self.loglines[line_no]
        fields = utils.parse_logline(logline)

        self.assertEqual(self.bot_id, fields["bot_id"],
                         "bot_id %s didn't match %s"
                         "".format(self.bot_id, fields["bot_id"]))

        self.assertEqual(levelname, fields["log_level"])
        self.assertEqual(message, fields["message"])

    def assertLoglineMatches(self, line_no, pattern, levelname="ERROR"):
        """Asserts if a logline matches a specific requirement.
           Args:
                line_no: Number of the logline which is asserted
                pattern: Message text which is compared
                type: Type of logline which is asserted"""

        self.assertIsNotNone(self.loglines)
        logline = self.loglines[line_no]
        fields = utils.parse_logline(logline)

        self.assertEqual(self.bot_id, fields["bot_id"],
                         "bot_id %s didn't match %s"
                         "".format(self.bot_id, fields["bot_id"]))

        self.assertEqual(levelname, fields["log_level"])
        self.assertRegex(fields["message"], pattern)

    def assertRegexpMatchesLog(self, pattern):
        """Asserts that pattern matches against log. """

        self.assertIsNotNone(self.loglines_buffer)
        self.assertRegex(self.loglines_buffer, pattern)

    def assertNotRegexpMatchesLog(self, pattern):
        """Asserts that pattern doesn't match against log."""

        self.assertIsNotNone(self.loglines_buffer)
        try:
            self.assertNotRegexpMatches(self.loglines_buffer, pattern)
        except AttributeError:
            self.assertNotRegex(self.loglines_buffer, pattern)

    def assertOutputQueueLen(self, queue_len=0):
        """
        Asserts that the output queue has the expected length.
        """
        self.assertEqual(len(self.get_output_queue()), queue_len)

    def assertMessageEqual(self, queue_pos, expected_msg):
        """
        Asserts that the given expected_message is
        contained in the generated event with
        given queue position.
        """
        event = self.get_output_queue()[queue_pos]
        self.assertIsInstance(event, str)

        event_dict = json.loads(event)
        expected = expected_msg.copy()
        del event_dict['time.observation']
        del expected['time.observation']

        self.assertDictEqual(expected, event_dict)
