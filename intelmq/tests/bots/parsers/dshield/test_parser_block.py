# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.dshield.parser_block import DshieldBlockParserBot


class TestDshieldBlockParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DshieldBlockParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = DshieldBlockParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
