# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malc0de.parser_ip_blacklist import \
    Malc0deIPBlacklistParserBot


class TestMalc0deIPBlacklistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Malc0deIPBlacklistParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = Malc0deIPBlacklistParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
