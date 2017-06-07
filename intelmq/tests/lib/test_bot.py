# -*- coding: utf-8 -*-
"""
Tests the Bot class itself.
"""

import unittest
import unittest.mock as mock


import intelmq.lib.test as test
from intelmq.tests.lib import test_parser_bot


class TestBot(test.BotTestCase, unittest.TestCase):
    """ Testing generic funtionalties of Bot base class. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = test_parser_bot.DummyParserBot
        cls.allowed_error_count = 1

    def test_bot_name(self):
        pass

    def test_pipeline_raising(self):
        self.sysconfig = {"raise_on_connect": True}
        self.default_input_message = None
        self.run_bot(error_on_pipeline=True)
        self.assertLogMatches(levelname='ERROR', pattern='Pipeline failed')

    def test_pipeline_empty(self):
        self.default_input_message = None
        self.run_bot()
        self.assertLogMatches(levelname='ERROR', pattern='Bot has found a problem')

    def test_logging_level_other(self):
        self.sysconfig = {"logging_level": "DEBUG"}
        self.input_message = test_parser_bot.EXAMPLE_SHORT
        self.run_bot()
        self.assertLogMatches(levelname='DEBUG', pattern='test')


if __name__ == '__main__':  # pragma: no cover  # pragma: no cover
    unittest.main()
