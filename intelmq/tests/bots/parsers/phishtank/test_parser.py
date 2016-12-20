# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.phishtank.parser import PhishTankParserBot


class TestPhishTankParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for PhishTankParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = PhishTankParserBot

    def test_empty(self):
        self.run_bot()

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
