# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_ip import AbusechIPParserBot

with open(os.path.join(os.path.dirname(__file__), 'feodoips.txt')) as handle:
    EXAMPLE_FEODO_FILE = handle.read()
LINES = EXAMPLE_FEODO_FILE.splitlines()
HEADER = '\n'.join(LINES[:8]) + '\n' +  LINES[-1] + '\n' + LINES[-4].replace('"', '') + '\n'

EXAMPLE_FEODO_REPORT = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                        "feed.name": "AbuseCH Feodotracker",
                        "time.observation": "2019-03-01T01:01:01+00:00",
                        "__type": "Report",
                        "raw": utils.base64_encode(EXAMPLE_FEODO_FILE)
                       }

EXAMPLE_FEODO_EVENT = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                       "feed.name": "AbuseCH Feodotracker",
                       "source.ip": "10.213.75.205",
                       "source.port": 443,
                       "raw": utils.base64_encode(HEADER + LINES[9].replace('"', '')),
                       "time.observation": "2019-03-01T01:01:01+00:00",
                       "extra.first_seen": "2021-01-17T07:30:05+00:00",
                       "extra.last_online": "2021-02-10T00:00:00+00:00",
                       "extra.feed_last_generated": "2021-02-10T13:34:57+00:00",
                       "time.source": "2021-02-10T00:00:00+00:00",
                       "classification.taxonomy": "malicious code",
                       "classification.type": "c2server",
                       "malware.name": "dridex",
                       "status": "online",
                       "__type": "Event"
                       }
EXAMPLE_FEODO_EVENT1 = {"feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
                        "feed.name": "AbuseCH Feodotracker",
                        "source.ip": "192.16.238.101",
                        "source.port": 443,
                        "raw": utils.base64_encode(HEADER + LINES[10].replace('"', '')),
                        "time.observation": "2019-03-01T01:01:01+00:00",
                        "extra.feed_last_generated": "2021-02-10T13:34:57+00:00",
                        "extra.first_seen": "2021-01-17T07:44:46+00:00",
                        "extra.last_online": "2021-02-10T00:00:00+00:00",
                        "time.source": "2021-02-10T00:00:00+00:00",
                        "classification.taxonomy": "malicious code",
                        "classification.type": "c2server",
                        "malware.name": "dridex",
                        "status": "online",
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
