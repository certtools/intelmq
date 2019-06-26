# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.viriback.parser import ViribackParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_viriback.data')) as handle:
    REPORT_DATA = handle.read()
    IOCS = REPORT_DATA.splitlines()[78].strip()[8:-10].split("</td></tr><tr><td>")
    

        

REPORT = {"__type": "Report",
          "feed.name": "Viriback",
          "feed.url": "http://tracker.viriback.com/",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }




EVENT1 = {"raw": utils.base64_encode(IOCS[0]),
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "http://tracker.viriback.com/",
          "source.url": "http://acptw.icu/clap/five/PvqDq929BSx_A_D_M1n_a.php",
          "source.ip": "62.173.140.190",
          "classification.taxonomy": "malicious code",
          "classification.type": "malware",
          "classification.identifier": "Lokibot",
          "feed.name": "Viriback"}

EVENT2 = {"raw": utils.base64_encode(IOCS[1]),
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "http://tracker.viriback.com/",
          "source.url": "http://ivandarina.top/jam/PvqDq929BSx_A_D_M1n_a.php",
          "source.ip": "198.23.213.114",
          "classification.taxonomy": "malicious code",
          "classification.type": "malware",
          "classification.identifier": "Lokibot",
          "feed.name": "Viriback"}

EVENT3 = {"raw": utils.base64_encode(IOCS[2]),
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "http://tracker.viriback.com/",
          "source.url": "http://adamsjef.top/jef/PvqDq929BSx_A_D_M1n_a.php",
          "source.ip": "198.23.213.114",
          "classification.taxonomy": "malicious code",
          "classification.identifier": "Lokibot",
          "classification.type": "malware",
          "feed.name": "Viriback"}


class TestViribackParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ViribackParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
