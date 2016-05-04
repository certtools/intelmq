# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.openbl.parser import OpenBLParserBot


class TestOpenBLParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for OpenBLParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenBLParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
