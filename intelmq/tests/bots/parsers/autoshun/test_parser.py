# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.autoshun.parser import AutoshunParserBot


class TestAutoshunParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AutoshunParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = AutoshunParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
