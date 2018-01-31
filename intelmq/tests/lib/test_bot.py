# -*- coding: utf-8 -*-
"""
Tests the Bot class itself.
"""

import unittest


import intelmq.lib.test as test
from intelmq.lib.bot import Bot
from intelmq.tests.lib import test_parser_bot


class TestBot(test.BotTestCase, unittest.TestCase):
    """ Testing generic functionalities of Bot base class. """

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

    def test_logging_catch_warnings(self):
        """
        Test if the logger catches warnings issued by the warnings module.
        """
        self.input_message = test_parser_bot.EXAMPLE_SHORT
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertLogMatches(levelname='WARNING', pattern='.*intelmq/tests/lib/test_parser_bot\.py\:77\: UserWarning: This is a warning test.')

    def test_bot_group(self):
        """
        Test if the bot's group is Parser.
        """
        self.prepare_bot()
        self.assertEqual(self.bot.group, 'Parser')


class DummyExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        self.send_message(event, queue=event['feed.code'] if 'feed.code' in event else None)


class TestDummyExpertBot(test.BotTestCase, unittest.TestCase):
    """ Testing generic functionalities of Bot base class. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = test_parser_bot.DummyParserBot
        cls.default_input_message = {'feed.name': 'Test'}
        cls.allowed_error_count = 1

    def test_bot_name(self):
        self.run_bot()
        self.assertEqual(self.bot.name, 'Test Bot')

    def test_pipeline_default(self):
        self.input_message = {'feed.name': 'Test'}
        # XXX
        self.run_bot()
        self.get_output_queue() # XX
        self.assertOutputQueueLen()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
