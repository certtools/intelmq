from intelmq.lib.pipeline import Pipeline
from intelmq.lib.utils import create_stream_logger, parse_logline

import unittest
import StringIO
import json


class TestPipeline(Pipeline):
    """This TestPipeline is a mock class for a pipeline,
       it behaves in most ways like a normal pipeline would do,
       with the exception that it doesn't need a message broker"""

    def __init__(self, state_dict):
        self.state = state_dict

    def connect(self):
        pass

    def disconnect(self):
        pass

    def sleep(self, intveral):
        # Passes through as we want a test to be deterministic
        pass

    def send(self, message):
        """Sends a message to the destination queues"""
        for destination_queue in self.destination_queues:
            if destination_queue in self.state:
                self.state[destination_queue].append(message)
            else:
                self.state[destination_queue] = [message]

    def receive(self):
        """Receives the last not yet acknowledged message"""
        if len(self.state.get(self.internal_queue, [])) > 0:
            return self.state[self.internal_queue].pop(0)

        # non blocking, we assume that the source queue ISN'T EMPTY
        # the current solution in the normal pipeline code
        # uses blocking as this is provided by the time of writing
        # by redis brpoplpush(,,0) the zero means that this code
        # will block forever.
        #
        # In a test scenario this is not what
        # we want, so I hope that people don't expect it to behave
        # as if it mimics every aspect of a normal pipeline.

        first_msg = self.state[self.source_queue].pop(0)

        if self.internal_queue in self.state:
            self.state[self.internal_queue].append(first_msg)
        else:
            self.state[self.internal_queue] = [first_msg]

        return first_msg

    def acknowledge(self):
        """Removes a message from the internal queue and returns it"""
        return self.state.get(self.internal_queue, [None]).pop(0)

    def count_queued_messages(self, queues):
        """Returns the amount of queued messages
           over all given queue names.
           But only without a real message broker behind.
           As this is only for tests"""

        qdict = dict()
        for queue in queues:
            qdict[queue] = len(self.state.get(queue, []))
        return qdict


# other nice test related utility functions
def create_bot_test_configuration(bot_id, log_stream, state, params={}):
    """Creates a configuration which can be feed into a bot for
       testing it in an unit test"""

    config = {}

    config["system"] = {"logging_level": "DEBUG",
                        "logging_path": "/opt/intelmq/var/log/",  # not used
                        "http_proxy":  None,
                        "https_proxy": None}

    config["runtime"] = {bot_id: params,
                         "__default__": {"rate_limit": 0,
                                         "retry_delay": 0}}
    config["pipeline"] = {bot_id: {"source-queue": ("%s-input" % bot_id),
                                   "destination-queues": ["%s-output" % bot_id]}}

    config["logger"] = create_stream_logger(log_stream, bot_id)

    config["source_pipeline"] = TestPipeline(state)
    config["destination_pipeline"] = TestPipeline(state)

    assert(config["source_pipeline"].state is config["destination_pipeline"].state)

    return config


class BotTestCase(unittest.TestCase):
    """Models a TestCase for a bot"""

    def __init__(self, *args):
        super(BotTestCase, self).__init__(*args)

        self.maxDiff = None  # We want long diffs
        self.__clear_bot()

    def __clear_bot(self):
        """Resets the internal bot state back to empty state"""

        self.bot_id = "test-bot"
        self.bot_type = None

    def reset_bot(self):
        """Reconfigures the bot with the changed attributes"""

        self._queue_state = {}
        self.log_stream = StringIO.StringIO()

        self.config = create_bot_test_configuration(self.bot_id,
                                                    self.log_stream,
                                                    self._queue_state)

        self.bot = self.bot_type(self.bot_id, config=self.config)

        # run it only once, no loop please
        # no blocking, no hassle testing it
        self.bot.run_once = True

    def run_bot(self):
        """Call this method for actually doing a test
           run for the specified bot"""

        self.bot.start()
        self.loglines_buffer = self.log_stream.getvalue()

        self.loglines = self.loglines_buffer.splitlines()

    def get_input_queue(self):
        """Returns the input queue of this bot which can be filled
           with fixture data in setUp()"""

        return self._queue_state["%s-input" % self.bot_id]

    def set_input_queue(self, seq):
        """Setter for the input queue of this bot"""
        self._queue_state["%s-input" % self.bot_id] = seq

    input_queue = property(get_input_queue, set_input_queue)

    def get_output_queue(self):
        """Getter for the input queue of this bot. Use in TestCase scenarios"""
        return self._queue_state["%s-output" % self.bot_id]

    # custom assertions
    def assertLoglineEqual(self, line_no, message, levelname="ERROR"):
        """Asserts if a logline matches a specific requirement.

           Args:
                line_no: Number of the logline which is asserted
                message: Message text which is compared
                type: Type of logline which is asserted"""

        self.assertIsNotNone(self.loglines)
        logline = self.loglines[line_no]
        fields = parse_logline(logline)

        self.assertEqual(self.bot_id, fields["name"],
                         "bot_id %s didn't match %s" % (self.bot_id, fields["name"]))

        self.assertEqual(levelname, fields["levelname"])
        self.assertEqual(message, fields["message"])

    def assertRegexpMatchesLog(self, pattern):
        """Asserts that pattern matches against log"""

        self.assertIsNotNone(self.loglines_buffer)
        self.assertRegexpMatches(self.loglines_buffer, pattern)

    def assertNotRegexpMatchesLog(self, pattern):
        """Asserts that pattern doesn't match against log"""

        self.assertIsNotNone(self.loglines_buffer)
        self.assertNotRegexpMatches(self.loglines_buffer, pattern)

    def assertLogLengthEqual(self, log_length):
        """Asserts that the log has a certain length of lines"""

        msg =  ("Log of bot '%s' didn't match expected length"
                " (%d) of actual %d lines:\n %s") % (self.bot_id,
                                                     log_length,
                                                     len(self.loglines),
                                                     self.loglines_buffer)

        self.assertEqual(log_length, len(self.loglines), msg)

    def assertEventAlmostEqual(self, queue_pos, expected_event):
        """Asserts that the given expected_event is
           contained in the generated event with
           given queue position"""

        event = self.get_output_queue()[queue_pos]
        unicode_event = {}

        # FIXME when moving to python3:
        # just for convenience and for later python3 migration,
        # as python3 doesn't have unicode strings, just strings
        for key, value in expected_event.items():
            unicode_event[unicode(key)] = unicode(value)

        self.assertIsInstance(event, unicode)
        event_dict = json.loads(event)

        self.assertDictContainsSubset(unicode_event, event_dict)
