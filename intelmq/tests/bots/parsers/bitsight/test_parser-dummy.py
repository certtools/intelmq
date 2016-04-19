# -*- coding: utf-8 -*-


import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.bitsight.parser import BitsightParserBot


class TestBitsightParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for MalwareDomainsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BitsightParserBot
        cls.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()


