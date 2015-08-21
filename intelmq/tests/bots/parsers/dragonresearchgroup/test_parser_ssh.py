# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.dragonresearchgroup.parser_ssh import DragonResearchGroupSSHParserBot


class TestDragonResearchGroupSSHParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DragonResearchGroupSSHParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = DragonResearchGroupSSHParserBot
        self.default_input_message = json.dumps({'__type': 'Report'})

if __name__ == '__main__':
    unittest.main()
