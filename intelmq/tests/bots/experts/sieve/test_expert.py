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

EXAMPLE_MD5 = {"__type": "Event",
               "malware.hash.md5": "0904631316551",
               }


@test.skip_exotic()
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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_precedence.sieve')

        # test && has higher precedence than ||
        event = EXAMPLE_INPUT.copy()
        event['feed.provider'] = 'acme'
        expected = event.copy()
        expected['comment'] = 'match1'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # test round braces to change precedence
        event = EXAMPLE_INPUT.copy()
        event['source.abuse_contact'] = 'abuse@example.com'
        event['source.ip'] = '5.6.7.8'
        expected = event.copy()
        expected['comment'] = 'match2'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

    def test_string_equal_match(self):
        """ Test == string match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_equal_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.fqdn'] = 'www.example.com'
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test (key doesn't match)
        event = EXAMPLE_INPUT.copy()
        event['source.fqdn'] = 'www.hotmail.com'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

        # negative test (key not defined)
        event = EXAMPLE_INPUT.copy()
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_string_not_equal_match(self):
        """ Test != string match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_not_equal_match.sieve')

        # positive test (key mismatch)
        event = EXAMPLE_INPUT.copy()
        event['source.fqdn'] = 'mail.ru'
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # positive test (key undefined)
        event = EXAMPLE_INPUT.copy()
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test
        event = EXAMPLE_INPUT.copy()
        event['source.fqdn'] = 'www.example.com'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_string_contains_match(self):
        """ Test :contains string match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_contains_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'https://www.switch.ch/security/'
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test (key mismatch)
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'https://www.ripe.net/'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

        # negative test (key undefined)
        event = EXAMPLE_INPUT.copy()
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_string_notcontains_match(self):
        """ Test :notcontains string match."""
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_notcontains_match.sieve')

        # positive test (key undefined)
        event = EXAMPLE_INPUT.copy()
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # positive test (key mismatch)
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'https://www.switch.ch/security/'
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test (key match)
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'https://www.google.com/'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)


    def test_string_regex_match(self):
        """ Test =~ string match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_regex_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'https://www.switch.ch/security'
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test (key mismatch)
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'http://www.example.com'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

        # negative test (key undefined)
        event = EXAMPLE_INPUT.copy()
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_string_inverse_regex_match(self):
        """ Test !~ string match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_inverse_regex_match.sieve')

        # positive test (key mismatch)
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'http://www.example.com'
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # positive test (key undefined)
        event = EXAMPLE_INPUT.copy()
        expected = event.copy()
        expected['comment'] = 'match'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test (key match)
        event = EXAMPLE_INPUT.copy()
        event['source.url'] = 'https://www.switch.ch/security'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_string_invalid_ipaddr(self):
        """ Tests validation of harmonization for IP addresses. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_invalid_ipaddr.sieve')

        event = EXAMPLE_INPUT.copy()
        self.input_message = event
        with self.assertRaises(ValueError) as context:
            self.run_bot()
        exception = context.exception
        self.assertRegex(str(exception), 'Invalid ip address:')

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

    def test_numeric_invalid_key(self):
        """ Tests validation of harmonization for numeric types. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_invalid_key.sieve')

        event = EXAMPLE_INPUT.copy()
        self.input_message = event
        with self.assertRaises(ValueError) as context:
            self.run_bot()
        exception = context.exception
        self.assertRegex(str(exception), '.*Incompatible type: FQDN\.$')

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
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_string_match_value_list.sieve')

        # Match the first rule
        string_value_list_match_1 = EXAMPLE_INPUT.copy()
        string_value_list_match_1['classification.type'] = 'malware'
        string_value_list_expected_result_1 = string_value_list_match_1.copy()
        string_value_list_expected_result_1['comment'] = 'infected hosts'
        self.input_message = string_value_list_match_1
        self.run_bot()
        self.assertMessageEqual(0, string_value_list_expected_result_1)

        # Match the second rule
        string_value_list_match_2 = EXAMPLE_INPUT.copy()
        string_value_list_match_2['classification.type'] = 'c&c'
        string_value_list_expected_result_2 = string_value_list_match_2.copy()
        string_value_list_expected_result_2['comment'] = 'malicious server / service'
        self.input_message = string_value_list_match_2
        self.run_bot()
        self.assertMessageEqual(0, string_value_list_expected_result_2)

        # don't match any rule
        string_value_list_match_3 = EXAMPLE_INPUT.copy()
        string_value_list_match_3['classification.type'] = 'blacklist'
        self.input_message = string_value_list_match_3
        self.run_bot()
        self.assertMessageEqual(0, string_value_list_match_3)

    def test_numeric_match_value_list(self):
        """ Test numeric match with NumericValueList """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_match_value_list.sieve')

        # Match the first rule
        numeric_value_list_match_1 = EXAMPLE_INPUT.copy()
        numeric_value_list_match_1['destination.asn'] = 6939
        numeric_value_list_expected_result_1 = numeric_value_list_match_1.copy()
        numeric_value_list_expected_result_1['comment'] = 'Belongs to peering group'
        self.input_message = numeric_value_list_match_1
        self.run_bot()
        self.assertMessageEqual(0, numeric_value_list_expected_result_1)

        # Match the second rule
        numeric_value_list_match_2 = EXAMPLE_INPUT.copy()
        numeric_value_list_match_2['destination.asn'] = 1930
        numeric_value_list_expected_result_2 = numeric_value_list_match_2.copy()
        numeric_value_list_expected_result_2['comment'] = 'Belongs constituency group'
        self.input_message = numeric_value_list_match_2
        self.run_bot()
        self.assertMessageEqual(0, numeric_value_list_expected_result_2)

        # don't Match any rule
        numeric_value_list_match_3 = EXAMPLE_INPUT.copy()
        numeric_value_list_match_3['destination.asn'] = 3356
        self.input_message = numeric_value_list_match_3
        self.run_bot()
        self.assertMessageEqual(0, numeric_value_list_match_3)

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

    def test_update(self):
        """ Test updating key/value pairs """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_update.sieve')

        # If doesn't match, nothing should have changed
        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        # If expression matches && parameter doesn't exists, nothing changes
        event1['comment'] = 'update new parameter'
        result = event1.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, result)

        # If expression matches && parameter exists, source.ip changed
        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'update existing parameter'
        result2 = event2.copy()
        result2['source.ip'] = '10.9.8.7'
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, result2)

    def test_remove(self):
        """ Test removing keys """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_remove.sieve')

        # If doesn't match, nothing should have changed
        event1 = EXAMPLE_INPUT.copy()
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, event1)

        # If expression matches && parameter exists, parameter is removed
        event1['comment'] = 'remove parameter'
        result = event1.copy()
        event1['destination.ip'] = '192.168.10.1'
        self.input_message = event1
        self.run_bot()
        self.assertMessageEqual(0, result)

        # If expression matches && parameter doesn't exist, nothing happens
        event2 = EXAMPLE_INPUT.copy()
        event2['comment'] = 'remove parameter'
        result2 = event2.copy()
        self.input_message = event2
        self.run_bot()
        self.assertMessageEqual(0, result2)

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

    def test_ip_range_match(self):
        """ Test IP range match operator. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_ip_range_match.sieve')

        # match /24 network
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '192.0.0.1'
        expected = event.copy()
        expected['comment'] = 'bogon1'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # match /16 network
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '192.0.200.1'
        expected = event.copy()
        expected['comment'] = 'bogon2'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # no match
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '192.168.0.1'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

        # IPv6 address
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '2001:620:0:ff::56'
        expected = event.copy()
        expected['comment'] = 'SWITCH'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # invalid address in event should not match
        event = EXAMPLE_INPUT.copy()
        event['comment'] = '300.300.300.300'
        self.input_message = event
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertLogMatches(pattern='^Could not parse IP address', levelname='WARNING')
        self.assertMessageEqual(0, event)

    def test_ip_range_list_match(self):
        """ Test IP range list match operator. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_ip_range_list_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '192.0.0.1'
        expected = event.copy()
        expected['comment'] = 'bogon'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '8.8.8.8'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_network_host_bits_list_match(self):
        """ Test if range list of networks with host bits set match operator. """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_ip_range_list_match.sieve')

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '169.254.2.1'
        expected = event.copy()
        expected['comment'] = 'bogon'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # positive test
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '169.254.3.1'
        expected = event.copy()
        expected['comment'] = 'bogon'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

        # negative test
        event = EXAMPLE_INPUT.copy()
        event['source.ip'] = '169.255.2.1'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_comments(self):
        """ Test comments in sieve file."""
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__), 'test_sieve_files/test_comments.sieve')

        event = EXAMPLE_INPUT.copy()
        expected = event.copy()
        expected['comment'] = 'hello'
        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, expected)

    def test_named_queues(self):
        """ Test == numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_named_queues.sieve')

        # if match drop
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['comment'] = "drop"
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertOutputQueueLen(0)


        # if doesn't match keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['comment'] = "keep without path"
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_false)

        # if doesn't match keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['comment'] = "keep with path"
        self.input_message = numeric_match_false
        self.run_bot()

        # if doesn't match keep
        numeric_match_false = EXAMPLE_INPUT.copy()
        numeric_match_false['comment'] = "default path"
        self.input_message = numeric_match_false
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_false, path="_default")

    def test_numeric_key(self):
        """ Test == numeric match """
        self.sysconfig['file'] = os.path.join(os.path.dirname(__file__),
                                              'test_sieve_files/test_numeric_key.sieve')

        # if match drop
        numeric_match_true = EXAMPLE_INPUT.copy()
        numeric_match_true['comment'] = "drop"
        self.input_message = numeric_match_true
        self.run_bot()
        self.assertMessageEqual(0, numeric_match_true)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
