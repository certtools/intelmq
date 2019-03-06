# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_ip import AbusechIPParserBot

with open(os.path.join(os.path.dirname(__file__), 'feodoips.txt')) as handle:
    EXAMPLE_FEODO_FILE = handle.read()

EXAMPLE_FEODO_REPORT = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                        "feed.name": "AbuseCH Feodotracker",
                        "__type": "Report",
                        "raw": utils.base64_encode(EXAMPLE_FEODO_FILE),
                        "time.observation": "2015-11-02T13:11:44+00:00"
                       }

EXAMPLE_FEODO_EVENT = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                       "feed.name": "AbuseCH Feodotracker",
                       "source.ip": "110.93.230.101",
                       "source.port": 990,
                       "raw": utils.base64_encode("2019-03-05 22:10:24,110.93.230.101,990,Heodo"),
                       "time.observation": "2015-11-02T13:11:44+00:00",
                       "time.source": "2019-03-05T22:10:24+00:00",
                       "classification.taxonomy": "malicious code",
                       "classification.type": "c&c",
                       "malware.name": "heodo",
                       "__type": "Event"
                       }


class TestAbusechIPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusechIPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechIPParserBot
        cls.default_input_message = EXAMPLE_FEODO_REPORT

    def test_feodo_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_FEODO_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
