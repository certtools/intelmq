# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.hphosts.parser import HpHostsParserBot

with open(os.path.join(os.path.dirname(__file__), 'hosts.txt'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'blacklist',
           'raw': 'MTI3LjAuMC4xCWV4YW1wbGUuY29t',
           'source.fqdn': 'example.com'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'blacklist',
           'raw': 'MTI3LjAuMC4xCWV4YW1wbGUuaW52YWxpZA==',
           'source.fqdn': 'example.invalid'}


class TestHpHostsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HpHostsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HpHostsParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
