
# -*- coding: utf-8 -*-
"""
Utilities for testing intelmq.

TheBotTestCase can be used as base class for unittests on bots. It includes
some basic generic tests (logged errors, correct pipeline setup).
"""
from __future__ import unicode_literals

import io
import json
import logging
import unittest

import intelmq.lib.message as message
import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
import mock
from intelmq import PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, SYSTEM_CONF_FILE


def mocked_config(bot_id, src_name, dst_names, sysconfig):
    def mock(conf_file):
        if conf_file == PIPELINE_CONF_FILE:
            return {bot_id: {"source-queue": src_name,
                             "destination-queues": dst_names},
                    }
        elif conf_file == RUNTIME_CONF_FILE:
            return {bot_id: {}}
        elif conf_file == SYSTEM_CONF_FILE:
            conf = {"logging_level": "DEBUG",
                    "http_proxy":  None,
                    "https_proxy": None,
                    "broker": "pythonlist",
                    "rate_limit": 0,
                    "retry_delay": 0,
                    "error_retry_delay": 0,
                    "error_max_retries": 0,
                    "exit_on_stop": False,
                    "redis_cache_host": "localhost",
                    "redis_cache_port": 6379,
                    "redis_cache_db": "10",
                    "redis_cache_ttl": 10,
                    }
            conf.update(sysconfig)
            return conf
        else:
            with open(conf_file, 'r') as fpconfig:
                config = json.loads(fpconfig.read())
            return config
    return mock


def mocked_logger(logger):
    def log(path, name, level):
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

        cls.set_bot()

        cls.bot_name = cls.bot_reference.__name__
        if cls.bot_type is None:
            for type_name, type_match in cls.bot_types.items():
                if cls.bot_name.endswith(type_match):
                    cls.bot_type = type_name
                    break

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
            self.input_queue = [self.input_message]
            self.input_message = None
        else:
            self.input_queue = [self.default_input_message]

    def run_bot(self):
        """
        Call this method for actually doing a test run for the specified bot.
        """
        self.prepare_bot()
        with mock.patch('intelmq.lib.utils.load_configuration',
                        new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.mocked_log):
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
        self.pipe.state["%s-input" % self.bot_id] = seq

    input_queue = property(get_input_queue, set_input_queue)

    def get_output_queue(self):
        """Getter for the input queue of this bot. Use in TestCase scenarios"""
        return self.pipe.state["%s-output" % self.bot_id]

    def test_bot_start(self):
        """Tests if we can start a bot and feed data into
            it and have a reasonable output"""
        self.run_bot()

    def test_log_starting(self):
        """ Test if bot logs starting message. """
        self.run_bot()
        self.assertLoglineEqual(0, "Bot is starting", "INFO")

    def test_log_not_error(self):
        """ Test if bot does not log errors. """
        self.run_bot()
        self.assertNotRegexpMatches(self.loglines_buffer, "ERROR")

    def test_log_not_critical(self):
        """ Test if bot does not log critical errors. """
        self.run_bot()
        self.assertNotRegexpMatches(self.loglines_buffer, "CRITICAL")

    def test_pipe_names(self):
        """ Test if all pipes are created with correct names. """
        self.run_bot()
        pipenames = ["{}-input", "{}-input-internal", "{}-output"]
        self.assertListEqual([x.format(self.bot_id) for x in pipenames],
                             list(self.pipe.state.keys()))

    def test_empty_message(self):
        """
        Test if bot fails when receiving an empty message.

        Bot.receive_message() returns None if the message evaluates to False
        e.g. if empty. Bots have to handle this situation.
        """
        if self.bot_type == 'collector':
            raise unittest.SkipTest('Given Bot is Collector.')

        self.input_message = ''
        self.run_bot()
        self.assertRegexpMatchesLog("WARNING - Empty message received.")
        self.assertNotRegexpMatches(self.loglines_buffer, "ERROR")

    def test_bot_name(self):
        """
        Test if Bot has a valid name.
        Must be CamelCase and end with CollectorBot etc.
        Test class name must be Test{botclassname}
        """
        counter = 0
        for type_name, type_match in self.bot_types.items():
            try:
                self.assertRegexpMatches(self.bot_name,
                                         r'\A[a-zA-Z0-9]+{}\Z'
                                         r''.format(type_match))
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
            raise unittest.SkipTest('Given Bot is not a Collector.')

        self.run_bot()
        for report_json in self.get_output_queue():
            report = message.MessageFactory.unserialize(report_json)
            self.assertIsInstance(report, message.Report)
            self.assertIn('feed.name', report)
            self.assertIn('feed.url', report)
            self.assertIn('raw', report)

    def test_event(self):
        """ Test if event has required fields. """
        if self.bot_type not in ['parser', 'expert']:
            raise unittest.SkipTest('Given Bot is not a Parser or Expert.')

        self.run_bot()
        for event_json in self.get_output_queue():
            event = message.MessageFactory.unserialize(event_json)
            self.assertIsInstance(event, message.Event)
            self.assertIn('classification.type', event)
            self.assertIn('feed.url', event)
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

        self.assertEqual(self.bot_id, fields["name"],
                         "bot_id %s didn't match %s"
                         "".format(self.bot_id, fields["name"]))

        self.assertEqual(levelname, fields["levelname"])
        self.assertEqual(message, fields["message"])

    def assertRegexpMatchesLog(self, pattern):
        """Asserts that pattern matches against log. """

        self.assertIsNotNone(self.loglines_buffer)
        self.assertRegexpMatches(self.loglines_buffer, pattern)

    def assertNotRegexpMatchesLog(self, pattern):
        """Asserts that pattern doesn't match against log"""

        self.assertIsNotNone(self.loglines_buffer)
        self.assertNotRegexpMatches(self.loglines_buffer, pattern)

    def assertEventAlmostEqual(self, queue_pos, expected_event):
        """Asserts that the given expected_event is
           contained in the generated event with
           given queue position"""

        event = self.get_output_queue()[queue_pos]
        unicode_event = {}

        for key, value in expected_event.items():
            unicode_event[unicode(key)] = unicode(value)

        self.assertIsInstance(event, unicode)
        event_dict = json.loads(event)

        self.assertDictContainsSubset(unicode_event, event_dict)
