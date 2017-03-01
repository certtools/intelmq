# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.danger_rulez.parser import BruteForceBlockerParserBot

RAW = ("IyBJUAkJCSMgTGFzdCBSZXBvcnRlZAkJCUNvdW50CUlECjIwMy4wLjExMy40OAkJIyAyMDE2LTEx"
       "LTEwIDA5OjExOjAzCQk1NgkxMTAxOTczCjE5OC4xOC4wLjg5CQkjIDIwMTYtMTEtMDUgMDc6MDE6"
       "MTUJCTQzCTEwOTc5ODcK")

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'brute-force',
           'raw': 'MjAzLjAuMTEzLjQ4CQkjIDIwMTYtMTEtMTAgMDk6MTE6MDMJCTU2CTExMDE5NzM=',
           'source.ip': '203.0.113.48',
           'time.source': '2016-11-10T09:11:03+00:00'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'brute-force',
           'raw': 'MTk4LjE4LjAuODkJCSMgMjAxNi0xMS0wNSAwNzowMToxNQkJNDMJMTA5Nzk4Nw==',
           'source.ip': '198.18.0.89',
           'time.source': '2016-11-05T07:01:15+00:00'}


class TestBruteForceBlockerParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BruteForceBlockerParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BruteForceBlockerParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
