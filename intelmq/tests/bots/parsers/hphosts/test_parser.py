# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.hphosts.parser import HpHostsParserBot


class TestHpHostsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HpHostsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HpHostsParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
