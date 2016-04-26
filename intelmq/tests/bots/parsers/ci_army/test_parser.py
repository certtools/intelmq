# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.ci_army.parser import CIArmyParserBot


class TestCIArmyParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CIArmyParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CIArmyParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
