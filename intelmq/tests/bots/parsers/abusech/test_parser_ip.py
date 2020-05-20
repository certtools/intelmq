# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_ip import AbusechIPParserBot

with open(os.path.join(os.path.dirname(__file__), 'feodoips.txt')) as handle:
    EXAMPLE_FEODO_FILE = handle.read()
LINES = EXAMPLE_FEODO_FILE.splitlines()
HEADER = '\n'.join(LINES[:9]) + '\n' +  LINES[-1] + '\n'

EXAMPLE_FEODO_REPORT = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                        "feed.name": "AbuseCH Feodotracker",
                        "time.observation": "2019-03-01T01:01:01+00:00",
                        "__type": "Report",
                        "raw": utils.base64_encode(EXAMPLE_FEODO_FILE)
                       }

EXAMPLE_FEODO_EVENT = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                       "feed.name": "AbuseCH Feodotracker",
                       "source.ip": "110.93.230.101",
                       "source.port": 990,
                       "raw": utils.base64_encode(HEADER + LINES[9]),
                       "time.observation": "2019-03-01T01:01:01+00:00",
                       "extra.first_seen": "2019-03-04T22:10:24+00:00",
                       "extra.last_online": "2019-03-05T00:00:00+00:00",
                       "extra.feed_last_generated": "2019-03-05T22:10:24+00:00",
                       "time.source": "2019-03-05T00:00:00+00:00",
                       "classification.taxonomy": "malicious code",
                       "classification.type": "c2server",
                       "malware.name": "heodo",
                       "__type": "Event"
                       }
EXAMPLE_FEODO_EVENT1 = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                        "feed.name": "AbuseCH Feodotracker",
                        "source.ip": "192.155.88.196",
                        "source.port": 8080,
                        "raw": utils.base64_encode(HEADER + LINES[10]),
                        "time.observation": "2019-03-01T01:01:01+00:00",
                        "extra.feed_last_generated": "2019-03-05T22:10:24+00:00",
                        "extra.first_seen": "2017-12-18T23:36:45+00:00",
                        "time.source": "2017-12-18T23:36:45+00:00",
                        "classification.taxonomy": "malicious code",
                        "classification.type": "c2server",
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
        """ Test Feodotracker IPs. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_FEODO_EVENT)
        self.assertMessageEqual(1, EXAMPLE_FEODO_EVENT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
