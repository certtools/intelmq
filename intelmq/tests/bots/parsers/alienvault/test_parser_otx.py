# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.alienvault.parser_otx import AlienVaultOTXParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'test_parser_otx.data')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "AlienVault OTX",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-09-02T14:17:58+00:00"
                  }
EXAMPLE_EVENT = {
    "__type": "Event",
    "extra": '{"author": "AlienVault", "pulse": "The Spy Kittens Are Back: '
             'Rocket Kitten 2"}',
    "comment": """Our findings show that Rocket Kitten is still active, retains
a growing level of persistence, and acts ever more aggressively in terms of
attack method. We also found that recent publications on the group’s activity
have done nothing to change their behavior or reduce their activity. They don’t
seem to bother to have to “disappear.” With this paper, we feel fairly certain
that Rocket Kitten’s prime targets are not companies and political
organizations as entire bodies but individuals that operate in strategically
interesting fields such as diplomacy, foreign policy research, and
defense-related businesses. We believe the espionage factor and political
context make their attacks unique and very different from traditional targeted
attacks.""".replace('\n', ' '),
    "feed.name": "AlienVault OTX",
    "classification.type": "blacklist",
    "source.url": "http://107.6.172.54/woolen/",
    "raw": "eyJfaWQiOiAiNTVlNmJmYjE0NjM3ZjIyY2I2MDU3NDY2IiwgImNyZWF0ZWQiOiAiMj"
           "AxNS0wOS0wMlQwOToyMTo1My4wOTMiLCAiZGVzY3JpcHRpb24iOiAiIiwgImluZGlj"
           "YXRvciI6ICJodHRwOi8vMTA3LjYuMTcyLjU0L3dvb2xlbi8iLCAidHlwZSI6ICJVUk"
           "wifQ==",
    "time.source": "2015-09-02T09:21:53+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00"
}


class TestAlienVaultOTXParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AlienVaultOTXParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AlienVaultOTXParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

if __name__ == '__main__':
    unittest.main()
