# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import os
import intelmq.lib.test as test
from intelmq.bots.experts.sieve.expert import SieveExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "127.0.0.1",
                 "source.abuse_contact": "abuse@example.com",
                 "time.observation": "2017-01-01T00:00:00+00:00",
                 }

class TestSieveExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SieveExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SieveExpertBot
        #cls.sysconfig = {'file': os.path.join(os.path.dirname(__file__), 'test.sieve')}

    def test_or_match(self):
        """ Test Or Operator in match"""

    def test_and_match(self):
        """ Test And Operator in match"""

    def test_precedence(self):
        """ Test precedence of operators """

    def test_string_equal_match(self):
        """ Test == string match """

    def test_string_not_equal_match(self):
        """ Test != string match """

    def test_string_contains_match(self):
        """ Test :contains string match """

    def test_string_regex_match(self):
        """ Test =~ string match """

    def test_string_inverse_regex_match(self):
        """ Test !~ string match """

    def test_numeric_equal_match(self):
        """ Test == numeric match """

    def test_numeric_not_equal_match(self):
        """ Test != numeric match """

    def test_numeric_less_than_match(self):
        """ Test < numeric match """

    def test_numeric_less_than_or_equal_match(self):
        """ Test <= numeric match """

    def test_numeric_greater_than_match(self):
        """ Test > numeric match """

    def test_numeric_greater_than_or_equal_match(self):
        """ Test >= numeric match """

    def test_exists_match(self):
        """ Test :exists match """

    def test_not_exists_match(self):
        """ Test :notexists match """

    def test_string_match_value_list(self):
        """ Test string match with StringValueList """

    def test_numeric_match_value_list(self):
        """ Test numeric match with StringValueList """

    def test_drop_event(self):
        """ Test if matched event is dropped. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_drop_event.sieve')

        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = "deleteme"
        self.input_message = event2
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_keep_event(self):
        """ Test if matched event is kept. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_keep_event.sieve')

        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = "keepme"
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, event2)

    def test_add(self):
        """ Test adding key/value pairs """

    def test_add_force(self):
        """ Test adding key/value pairs, overwriting existing key """

    def test_modify(self):
        """ Test modifying key/value pairs """

    def test_remove(self):
        """ Test removing keys """




if __name__ == '__main__':  # pragma: no cover
    unittest.main()
