# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.hphosts.parser import HpHostsParserBot


class TestHpHostsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HpHostsParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = HpHostsParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
