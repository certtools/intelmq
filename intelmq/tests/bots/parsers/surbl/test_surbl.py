# -*- coding: utf-8 -*-
from os import path
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.surbl.parser import SurblParserBot
from intelmq.lib import utils

with open(path.join(path.dirname(__file__), 'test_surbl.data'), encoding='UTF-8') as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "surbl",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }
EVENT1 = {"__type": "Event",
          "source.fqdn": "domain1",
          "classification.type": "blacklist",
          "feed.name": "surbl",
          "raw": utils.base64_encode(".domain1"),
          "time.observation": "2018-01-24T15:58:48+00:00"
          }
EVENT2 = {"__type": "Event",
          "source.fqdn": "domain2",
          "classification.type": "malware",
          "feed.name": "surbl",
          "raw": utils.base64_encode(".domain2"),
          "time.observation": "2018-01-24T15:58:48+00:00"
          }
EVENT3 = {"__type": "Event",
          "source.fqdn": "domain3",
          "classification.type": "phishing",
          "feed.name": "surbl",
          "raw": utils.base64_encode(".domain3"),
          "time.observation": "2018-01-24T15:58:48+00:00"
          }


class TestSurblParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SurblParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':
    unittest.main()
