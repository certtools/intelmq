# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.openphish.parser import OpenPhishParserBot


class TestOpenPhishParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for OpenPhishParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenPhishParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
