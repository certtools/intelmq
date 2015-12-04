# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cleanmx.parser_phishing import \
    CleanMXPhishingParserBot


class TestCleanMXPhishingParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CleanMXPhishingParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = CleanMXPhishingParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
