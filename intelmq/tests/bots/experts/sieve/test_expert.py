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

    def test_or_match(self):
        """ Test Or Operator in match"""
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_or_match.sieve')

        # Expressions: TRUE || TRUE => TRUE
        truetrue = EXAMPLE_INPUT.copy()
        truetrue['comment'] = "I am TRUE in OR clause"
        truetrue_result = truetrue.copy()
        truetrue_result['source.ip'] = "10.9.8.7"
        self.input_message = truetrue
        self.run_bot()
        self.assertMessageEqual(0, truetrue_result)

        # Expressions: TRUE || FALSE => TRUE
        truefalse = EXAMPLE_INPUT.copy()
        truefalse['comment'] = "I am NOT True in OR clause"
        truefalse_result = truefalse.copy()
        truefalse_result['source.ip'] = "10.9.8.7"
        self.input_message = truefalse
        self.run_bot()
        self.assertMessageEqual(0, truefalse_result)

        # Expressions: FALSE || TRUE => TRUE
        falsetrue = EXAMPLE_INPUT.copy()
        falsetrue['source.abuse_contact'] = "test@test.eu"
        falsetrue['comment'] = "I am TRUE in OR clause"
        falsetrue_result = falsetrue.copy()
        falsetrue_result['source.ip'] = "10.9.8.7"
        self.input_message = falsetrue
        self.run_bot()
        self.assertMessageEqual(0, falsetrue_result)

        # Expressions: FALSE || FALSE => FALSE
        falsefalse = EXAMPLE_INPUT.copy()
        falsefalse['source.abuse_contact'] = "test@test.eu"
        falsefalse['comment'] = "I am NOT True in OR clause"
        falsefalse_result = falsefalse.copy()
        self.input_message = falsefalse
        self.run_bot()
        self.assertMessageEqual(0, falsefalse_result)

    def test_and_match(self):
        """ Test And Operator in match"""
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_and_match.sieve')

        # Expressions: TRUE && TRUE => TRUE
        truetrue = EXAMPLE_INPUT.copy()
        truetrue['comment'] = "I am TRUE in AND clause"
        truetrue_result = truetrue.copy()
        truetrue_result['source.ip'] = "10.9.8.7"
        self.input_message = truetrue
        self.run_bot()
        self.assertMessageEqual(0, truetrue_result)

        # Expressions: TRUE && FALSE => FALSE
        truefalse = EXAMPLE_INPUT.copy()
        truefalse['comment'] = "I am NOT True in AND clause"
        truefalse_result = truefalse.copy()
        self.input_message = truefalse
        self.run_bot()
        self.assertMessageEqual(0, truefalse_result)

        # Expressions: FALSE && TRUE => FALSE
        falsetrue = EXAMPLE_INPUT.copy()
        falsetrue['source.abuse_contact'] = "test@test.eu"
        falsetrue['comment'] = "I am TRUE in AND clause"
        falsetrue_result = falsetrue.copy()
        self.input_message = falsetrue
        self.run_bot()
        self.assertMessageEqual(0, falsetrue_result)

        # Expressions: FALSE && FALSE => FALSE
        falsefalse = EXAMPLE_INPUT.copy()
        falsefalse['source.abuse_contact'] = "test@test.eu"
        falsefalse['comment'] = "I am NOT True in AND clause"
        falsefalse_result = falsefalse.copy()
        self.input_message = falsefalse
        self.run_bot()
        self.assertMessageEqual(0, falsefalse_result)

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_numeric_equal_match.sieve')

        # if match drop
        numeric_match_true=EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy']=100.0
        self.input_message=numeric_match_true
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if doesn't match keep
        numeric_match_false=EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy']=50.0
        self.input_message=numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0,numeric_match_false)

    def test_numeric_not_equal_match(self):
        """ Test != numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_numeric_not_equal_match.sieve')

        # if not equal drop
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 50.0
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if equal keep
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy'] = 100
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_true)

    def test_numeric_less_than_match(self):
        """ Test < numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_numeric_less_than_match.sieve')

        # if less than drop
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy'] = 50.0
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if greater than keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 99.5
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_false)

    def test_numeric_less_than_or_equal_match(self):
        """ Test <= numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_numeric_less_than_or_equal_match.sieve')

        # if less than drop
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 40.0
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if equal drop
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 90
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if greater than keep
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy'] = 95.0
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_true)

    def test_numeric_greater_than_match(self):
        """ Test > numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_numeric_greater_than_match.sieve')

        # if greater than drop
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy'] = 50.0
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if less than keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 35.5
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_false)

    def test_numeric_greater_than_or_equal_match(self):
        """ Test >= numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_numeric_greater_than_or_equal_match.sieve')

        # if less than keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 40.0
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_false)

        # if equal drop
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 90
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if greater than drop
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy'] = 95.0
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertOutputQueueLen(0)

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

    def test_multiple_actions(self):
        """ Test applying multiple actions in one rule """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_multiple_actions.sieve')

        event = EXAMPLE_INPUT.copy()
        event['classification.type'] = 'unknown'
        self.input_message = event
        self.run_bot()

        expected_result = event.copy()
        expected_result['source.ip'] = '127.0.0.2'
        expected_result['comment'] = 'added'
        del expected_result['classification.type']

        self.assertMessageEqual(0, expected_result)




if __name__ == '__main__':  # pragma: no cover
    unittest.main()
