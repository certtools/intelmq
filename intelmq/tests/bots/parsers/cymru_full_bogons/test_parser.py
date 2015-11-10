# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cymru_full_bogons.parser import \
    CymruFullBogonsParserBot


class TestCymruFullBogonsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CymruFullBogonsParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = CymruFullBogonsParserBot
        self.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
