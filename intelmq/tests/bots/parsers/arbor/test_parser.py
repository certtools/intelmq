# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.arbor.parser import ArborParserBot


class TestArborParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for ArborParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ArborParserBot
        cls.default_input_message = {'__type': 'Report'}

if __name__ == '__main__':
    unittest.main()
