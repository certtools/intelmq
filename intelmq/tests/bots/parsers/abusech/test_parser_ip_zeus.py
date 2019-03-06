# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_ip import AbusechIPParserBot

with open(os.path.join(os.path.dirname(__file__), 'zeusips.txt')) as handle:
    EXAMPLE_ZEUS_FILE = handle.read()

EXAMPLE_ZEUS_REPORT = {"feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist",
                        "feed.name": "AbuseCH Zeustracker",
                        "__type": "Report",
                        "raw": utils.base64_encode(EXAMPLE_ZEUS_FILE),
                        "time.observation": "2015-11-02T13:11:44+00:00"
                       }

EXAMPLE_ZEUS_EVENT = {"feed.url": "https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist",
                       "feed.name": "AbuseCH Zeustracker",
                       "source.ip": "101.200.81.187",
                       "raw": utils.base64_encode("101.200.81.187"),
                       "time.observation": "2015-11-02T13:11:44+00:00",
                       "classification.taxonomy": "malicious code",
                       "classification.type": "c&c",
                       "malware.name": "zeus",
                       "__type": "Event"
                       }


class TestAbusechIPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusechIPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechIPParserBot
        cls.default_input_message = EXAMPLE_ZEUS_REPORT

    def test_zeus_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_ZEUS_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
