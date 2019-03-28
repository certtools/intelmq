# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.threatminer.parser import ThreatminerParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_threatminer.data')) as handle:
    REPORT_DATA = handle.read()
    REPORT_DATA_SPLIT = REPORT_DATA.splitlines()

REPORT = {"__type": "Report",
          "feed.name": "Threatminer",
          "feed.url": "https://www.threatminer.org",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }
EVENT1 = {"__type": "Event",
          "classification.type": "blacklist",
          "feed.name": "Threatminer",
          "feed.url": "https://www.threatminer.org",
          "raw": utils.base64_encode(REPORT_DATA_SPLIT[453]),
          "source.fqdn": "11e.com",
          "time.observation": "2018-01-24T14:23:34+00:00",
          }
EVENT2 = {"__type": "Event",
          "classification.type": "blacklist",
          "feed.name": "Threatminer",
          "feed.url": "https://www.threatminer.org",
          "raw": utils.base64_encode(REPORT_DATA_SPLIT[455]),
          "source.fqdn": "studiosimge.com",
          "time.observation": "2018-01-24T14:23:34+00:00",
          }
EVENT3 = {"__type": "Event",
          "classification.type": "blacklist",
          "feed.name": "Threatminer",
          "feed.url": "https://www.threatminer.org",
          "raw": utils.base64_encode(REPORT_DATA_SPLIT[457]),
          "source.fqdn": "www.studiosimge.com",
          "time.observation": "2018-01-24T14:23:34+00:00",
          }


class TestThreatminerParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ThreatminerParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
