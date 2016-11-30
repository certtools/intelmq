# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malc0de.parser_ip_blacklist import \
    Malc0deIPBlacklistParserBot

with open(os.path.join(os.path.dirname(__file__), 'IP_Blacklist.txt'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'malware',
           'raw': 'MTkyLjg4Ljk5LjQ=',
           'source.ip': '192.88.99.4'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'malware',
           'raw': 'MTkyLjAuMC41',
           'source.ip': '192.0.0.5'}


class TestMalc0deIPBlacklistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Malc0deDomainBlacklistParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Malc0deIPBlacklistParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
