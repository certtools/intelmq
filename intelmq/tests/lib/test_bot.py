# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Tests the Bot class itself.
"""
import json
import unittest

import intelmq.lib.test as test
from intelmq.tests.lib import test_parser_bot
from intelmq.lib.message import MessageFactory, Message


class TestDummyParserBot(test.BotTestCase, unittest.TestCase):
    """ Testing generic functionalities of Bot base class. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = test_parser_bot.DummyParserBot

    def test_pipeline_raising(self):
        self.default_input_message = None
        self.run_bot(parameters={"raise_on_connect": True},
                     error_on_pipeline=True,
                     allowed_error_count=1)
        self.assertLogMatches(levelname='ERROR', pattern='Pipeline failed')

    def test_pipeline_empty(self):
        self.default_input_message = None
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(levelname='ERROR', pattern='.*pipeline failed.*')

    def test_logging_level_other(self):
        self.input_message = test_parser_bot.EXAMPLE_SHORT
        self.run_bot(parameters={"logging_level": "DEBUG"})
        self.assertLogMatches(levelname='DEBUG', pattern='test!')

    def test_logging_catch_warnings(self):
        """
        Test if the logger catches warnings issued by the warnings module.
        """
        self.input_message = test_parser_bot.EXAMPLE_SHORT
        self.run_bot(parameters={'raise_warning': True},
                     allowed_warning_count=1)
        self.assertLogMatches(levelname='WARNING', pattern=r'.*intelmq/tests/lib/test_parser_bot\.py\:[0-9]+\: UserWarning: This is a warning test.')

    def test_bot_group(self):
        """
        Test if the bot's group is Parser.
        """
        self.input_message = []
        self.prepare_bot()
        self.assertEqual(self.bot.group, 'Parser')

    def test_encoding_error_on_input_message(self):
        """
        Test if the bot is dumping / not retrying a message which is impossible to parse.
        https://github.com/certtools/intelmq/issues/1494
        """
        self.input_message = b'foo\xc9bar'
        self.run_bot(iterations=1, allowed_error_count=1)
        self.assertLogMatches(r'.*intelmq\.lib\.exceptions\.DecodingError:.*')
        self.assertEqual(self.pipe.state['test-bot-input-internal'], [])
        self.assertEqual(self.pipe.state['test-bot-input'], [])
        self.assertEqual(self.pipe.state['test-bot-output'], [])

    def test_invalid_value_on_input_message(self):
        """
        Test if the bot is dumping / not retrying a message which is impossible to parse.
        https://github.com/certtools/intelmq/issues/1765
        """
        self.input_message = b'{"source.asn": 0, "__type": "Event"}'
        self.run_bot(iterations=1, allowed_error_count=1)
        self.assertLogMatches(r'.*intelmq\.lib\.exceptions\.InvalidValue:.*')
        self.assertEqual(self.pipe.state['test-bot-input-internal'], [])
        self.assertEqual(self.pipe.state['test-bot-input'], [])
        self.assertEqual(self.pipe.state['test-bot-output'], [])


def send_message(self, *messages, path: str = "_default", auto_add=None,
                     path_permissive: bool = False):
    self._sent_messages.extend(messages)


BotLibSettings = {'logging_path': None,
                  'source_pipeline_broker': 'Pythonlistsimple',
                  'destination_pipeline_broker': 'Pythonlistsimple',
                  'destination_queues': {'_default': 'output',
                                         '_on_error': 'error'}}


class TestBotAsLibrary(unittest.TestCase):
    def assertMessageEqual(self, actual, expected):
        """
        Compare two messages as dicts.
        """
        if isinstance(actual, Message):
            actual = actual.to_dict(with_type=True)
        else:
            actual = actual.copy()

        if isinstance(expected, Message):
            expected = expected.to_dict(with_type=True)
        else:
            expected = expected.copy()

        if 'time.observation' in actual:
            del actual['time.observation']
        if 'time.observation' in expected:
            del expected['time.observation']
        if 'output' in actual:
            actual['output'] = json.loads(actual['output'])
        if 'output' in expected:
            expected['output'] = json.loads(expected['output'])

        self.assertDictEqual(actual, expected)

    """def test_dummy_mocked(self):
        bot = test_parser_bot.DummyParserBot('dummy-bot', settings={'global': {'logging_path': None, 'skip_pipeline': True, 'broker': 'pythonlist'}, 'dummy-bot': {}})
        bot._Bot__current_message = MessageFactory.from_dict(test_parser_bot.EXAMPLE_REPORT)
        bot._Bot__connect_pipelines = lambda self: None
        bot._sent_messages = []
        bot._dumped_messages = []
        bot.send_message = send_message.__get__(bot, test_parser_bot.DummyParserBot)
        bot._dump_message = _dump_message.__get__(bot, test_parser_bot.DummyParserBot)
        bot.process()
        assert bot._sent_messages == [MessageFactory.from_dict(test_parser_bot.EXAMPLE_EVENT)]
        assert bot._dumped_messages[0][1] == test_parser_bot.EXPECTED_DUMP[0]
        assert bot._dumped_messages[1][1] == test_parser_bot.EXPECTED_DUMP[1]"""

    def test_dummy_pythonlist(self):
        bot = test_parser_bot.DummyParserBot('dummy-bot', settings=BotLibSettings)
        sent_messages = bot.process_message(test_parser_bot.EXAMPLE_REPORT.copy())
        self.assertMessageEqual(sent_messages['output'][0], test_parser_bot.EXAMPLE_EVENT)
        self.assertMessageEqual(sent_messages['error'][0], MessageFactory.from_dict(test_parser_bot.EXPECTED_DUMP[0].copy(), default_type='Report'))
        self.assertMessageEqual(sent_messages['error'][1], MessageFactory.from_dict(test_parser_bot.EXPECTED_DUMP[1].copy(), default_type='Report'))

    def test_domain_suffix(self):
        from intelmq.bots.experts.domain_suffix.expert import DomainSuffixExpertBot
        domain_suffix = DomainSuffixExpertBot('domain-suffix',  # bot id
                                              settings=BotLibSettings | {'field': 'fqdn',
                                                                         'suffix_file': '/usr/share/publicsuffix/public_suffix_list.dat'})
        queues = domain_suffix.process_message({'source.fqdn': 'www.example.com'})
        assert queues['output'][0]['source.domain_suffix'] == 'com'


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
