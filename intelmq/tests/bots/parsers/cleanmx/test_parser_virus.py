# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cleanmx.parser_virus import CleanMXVirusParserBot


class TestCleanMXVirusParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CleanMXVirusParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CleanMXVirusParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

if __name__ == '__main__':
    unittest.main()
