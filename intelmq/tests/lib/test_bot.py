# -*- coding: utf-8 -*-
"""
Tests the Bot class itself.
"""

import unittest

import intelmq.lib.test as test
from intelmq.tests.lib import test_parser_bot


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
        self.assertLogMatches(levelname='WARNING', pattern='.*intelmq/tests/lib/test_parser_bot\.py\:[0-9]+\: UserWarning: This is a warning test.')

    def test_bot_group(self):
        """
        Test if the bot's group is Parser.
        """
        self.input_message = []
        self.prepare_bot()
        self.assertEqual(self.bot.group, 'Parser')

    def test_invalid_input_message(self):
        """
        Test if the bot is dumping / not retrying a message which is impossible to parse.
        https://github.com/certtools/intelmq/issues/1494
        """
        self.input_message = b'foo\xc9bar'
        self.run_bot(iterations=1, allowed_error_count=1)
        self.assertLogMatches('.*intelmq\.lib\.exceptions\.DecodingError:.*')
        self.assertEqual(self.pipe.state['test-bot-input-internal'], [])
        self.assertEqual(self.pipe.state['test-bot-input'], [])
        self.assertEqual(self.pipe.state['test-bot-output'], [])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
