# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        cls.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
