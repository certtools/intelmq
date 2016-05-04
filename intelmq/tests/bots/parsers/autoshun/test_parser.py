# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.autoshun.parser import AutoshunParserBot


class TestAutoshunParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AutoshunParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AutoshunParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
