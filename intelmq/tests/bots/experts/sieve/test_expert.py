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

    def test_if_clause(self):
        """ Test processing of subsequent if clauses. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_if_clause.sieve')

        # assert first if clause is matched
        event1 = EXAMPLE_INPUT.copy()
        event1['comment'] = 'changeme'
        expected1 = EXAMPLE_INPUT.copy()
        expected1['comment'] = 'changed'
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, expected1)

        # assert second if clause is matched
        event2 = EXAMPLE_INPUT.copy()
        event2['source.ip'] = '192.168.0.1'
        expected2 = EXAMPLE_INPUT.copy()
        expected2['source.ip'] = '192.168.0.2'
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, expected2)

        # assert both if clauses are matched
        event3 = EXAMPLE_INPUT.copy()
        event3['comment'] = 'changeme'
        event3['source.ip'] = '192.168.0.1'
        expected3 = EXAMPLE_INPUT.copy()
        expected3['comment'] = 'changed'
        expected3['source.ip'] = '192.168.0.2'
        self.input_message = event3
        self.run_bot()
        self.assertMessageEqual(0, expected3)

        # assert none of the if clauses matched
        event4 = EXAMPLE_INPUT.copy()
        self.input_message = event4
        self.run_bot()
        self.assertMessageEqual(0, event4)

    def test_if_else_clause(self):
        """ Test processing else clause. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_if_else_clause.sieve')

        # assert that event matches if clause
        event1 = EXAMPLE_INPUT.copy()
        event1['comment'] = 'match'
        expected1 = EXAMPLE_INPUT.copy()
        expected1['comment'] = 'matched'
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, expected1)

        # assert that action in else clause is applied
        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'foobar'
        expected2 = EXAMPLE_INPUT.copy()
        expected2['comment'] = 'notmatched'
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, expected2)

    def test_if_elif_clause(self):
        """ Test processing elif clauses. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_if_elif_clause.sieve')

        # test match if clause
        event = EXAMPLE_INPUT.copy()
        event['comment'] = 'match1'
        expected = EXAMPLE_INPUT.copy()
        expected['comment'] = 'changed1'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # test match first elif clause
        event['comment'] = 'match2'
        expected['comment'] = 'changed2'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # test match second elif clause
        event['comment'] = 'match3'
        expected['comment'] = 'changed3'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # test no match
        event['comment'] = 'foobar'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_if_elif_else_clause(self):
        """ Test processing if, elif, and else clause. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_if_elif_else_clause.sieve')

        # test match if clause
        event = EXAMPLE_INPUT.copy()
        event['comment'] = 'match1'
        expected = EXAMPLE_INPUT.copy()
        expected['comment'] = 'changed1'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # test match elif clause
        event['comment'] = 'match2'
        expected['comment'] = 'changed2'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # test match else clause
        event['comment'] = 'match3'
        expected['comment'] = 'changed3'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

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
        # TODO

    def test_string_equal_match(self):
        """ Test == string match """
        # TODO

    def test_string_not_equal_match(self):
        """ Test != string match """
        # TODO

    def test_string_contains_match(self):
        """ Test :contains string match """
        # TODO

    def test_string_regex_match(self):
        """ Test =~ string match """
        # TODO

    def test_string_inverse_regex_match(self):
        """ Test !~ string match """
        # TODO

    def test_numeric_equal_match(self):
        """ Test == numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_equal_match.sieve')

        # if match drop
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['feed.accuracy'] = 100.0
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertOutputQueueLen(0)

        # if doesn't match keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['feed.accuracy'] = 50.0
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_false)

    def test_numeric_not_equal_match(self):
        """ Test != numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_not_equal_match.sieve')

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_less_than_match.sieve')

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_less_than_or_equal_match.sieve')

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_greater_than_match.sieve')

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_greater_than_or_equal_match.sieve')

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_exists_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.fqdn'] = 'www.example.com'
        expected = event.copy()
        expected['comment'] = 'I think therefore I am.'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test
        event = EXAMPLE_INPUT.copy()
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_not_exists_match(self):
        """ Test :notexists match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_notexists_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        expected = event.copy()
        expected['comment'] = 'I think therefore I am.'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test
        event = EXAMPLE_INPUT.copy()
        event['source.fqdn'] = 'www.example.com'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_string_match_value_list(self):
        """ Test string match with StringValueList """
        # TODO

    def test_numeric_match_value_list(self):
        """ Test numeric match with StringValueList """
        # TODO

    def test_drop_event(self):
        """ Test if matched event is dropped and processing is stopped. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_drop_event.sieve')

        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'drop'
        self.input_message = event2
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_keep_event(self):
        """ Test if matched event is kept and processing is stopped. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_keep_event.sieve')

        event1 = EXAMPLE_INPUT.copy()
        event1['comment'] = 'continue'
        self.input_message = event1
        self.run_bot()
        expected1 = EXAMPLE_INPUT.copy()
        expected1['comment'] = 'changed'
        self.assertMessageEqual(0, expected1)

        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'keep'
        self.input_message = event2
        self.run_bot()
        expected2 = EXAMPLE_INPUT.copy()
        expected2['comment'] = 'keep'
        self.assertMessageEqual(0, expected2)

    def test_add(self):
        """ Test adding key/value pairs """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_add.sieve')

        # If doesn't match, nothing should have changed
        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        # If expression matches, destination.ip field is added
        event1['comment'] = 'add field'
        result = event1.copy()
        result['destination.ip'] = '150.50.50.10'
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, result)

    def test_add_force(self):
        """ Test adding key/value pairs, overwriting existing key """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_add_force.sieve')

        # If doesn't match, nothing should have changed
        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        # If expression matches, destination.ip field is added as new field
        event1['comment'] = 'add force new field'
        result = event1.copy()
        result['destination.ip'] = '150.50.50.10'
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, result)

        # If expression matches, destination.ip field is added as new field
        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'add force existing fields'
        result2 = event2.copy()
        result2['destination.ip'] = '200.10.9.7'
        result2['source.ip'] = "10.9.8.7"
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, result2)

    def test_modify(self):
        """ Test modifying key/value pairs """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_modify.sieve')

        # If doesn't match, nothing should have changed
        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        # If expression matches && parameter doesn't exists, nothing changes
        event1['comment'] = 'modify new parameter'
        result = event1.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, result)

        # If expression matches && parameter exists, source.ip changed
        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'modify existing parameter'
        result2 = event2.copy()
        result2['source.ip'] = '10.9.8.7'
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, result2)

    def test_remove(self):
        """ Test removing keys """
        # TODO

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
