# -*- coding: utf-8 -*-
"""
Tests the Bot class itself.
"""

import sys
import unittest

import intelmq.lib.test as test
from intelmq.tests.lib import test_parser_bot


class TestBot(test.BotTestCase, unittest.TestCase):
    """ Testing generic functionalities of Bot base class. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = test_parser_bot.DummyParserBot
        cls.allowed_error_count = 1

    def test_bot_name(self):
        pass

#    @test.skip_travis()
    @unittest.skip("Strange blocking behavior")
    def test_pipeline_raising(self):
        self.default_input_message = None
        self.run_bot(parameters={"raise_on_connect": True},
                     error_on_pipeline=True)
        self.assertLogMatches(levelname='ERROR', pattern='Pipeline failed')

    def test_pipeline_empty(self):
        self.default_input_message = None
        self.run_bot()
        self.assertLogMatches(levelname='ERROR', pattern='Bot has found a problem')

    @unittest.skipIf(sys.version_info[:2] == (3, 7),
                     'Unclear behavior with copies of logger in Python 3.7, see '
                     'https://bugs.python.org/issue9338 and https://github.com/certtools/intelmq/issues/1269')
    def test_logging_level_other(self):
        self.input_message = test_parser_bot.EXAMPLE_SHORT
        self.run_bot(parameters={"logging_level": "DEBUG"})
        self.assertLogMatches(levelname='DEBUG', pattern='test')

    def test_logging_catch_warnings(self):
        """
        Test if the logger catches warnings issued by the warnings module.
        """
        self.input_message = test_parser_bot.EXAMPLE_SHORT
        self.allowed_warning_count = 1
        self.run_bot(parameters={'raise_warning': True})
        self.assertLogMatches(levelname='WARNING', pattern='.*intelmq/tests/lib/test_parser_bot\.py\:[0-9]+\: UserWarning: This is a warning test.')

    def test_bot_group(self):
        """
        Test if the bot's group is Parser.
        """
        self.input_message = []
        self.prepare_bot()
        self.assertEqual(self.bot.group, 'Parser')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
