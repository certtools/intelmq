# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malc0de.parser_domain_blacklist import \
    Malc0deDomainBlacklistParserBot


class TestMalc0deDomainBlacklistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Malc0deDomainBlacklistParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = Malc0deDomainBlacklistParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
