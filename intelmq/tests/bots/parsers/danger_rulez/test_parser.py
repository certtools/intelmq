# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.danger_rulez.parser import BruteForceBlockerParserBot


class TestBruteForceBlockerParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BruteForceBlockerParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BruteForceBlockerParserBot

if __name__ == '__main__':
    unittest.main()
