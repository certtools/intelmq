# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.taichung.parser import TaichungCityNetflowParserBot


class TestTaichungCityNetflowParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TaichungCityNetflowParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TaichungCityNetflowParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
