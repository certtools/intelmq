# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.webinspektor.parser import WebinspektorParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_webinspektor.data')) as handle:
    REPORT_DATA = handle.read()
    REPORT_DATA_SPLIT = REPORT_DATA.splitlines()

REPORT = {"__type": "Report",
          "feed.name": "Webinspektor",
          "feed.url": "https://app.webinspector.com/public/recent_detections",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }
EVENT1 = {"raw": utils.base64_encode(REPORT_DATA_SPLIT[102].strip() + REPORT_DATA_SPLIT[104].strip()),
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "https://app.webinspector.com/public/recent_detections",
          "source.url": "https://cummins.inhance.io",
          "classification.taxonomy": "other",
          "classification.type": "blacklist",
          "classification.identifier": "Suspicious",
          "time.source": "2018-02-13T08:44:30+00:00",
          "feed.name": "Webinspektor"}
EVENT2 = {"raw": utils.base64_encode(REPORT_DATA_SPLIT[111].strip() + REPORT_DATA_SPLIT[113].strip()),
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "https://app.webinspector.com/public/recent_detections",
          "source.url": "http://naclkuso.myweb.hinet.net",
          "classification.taxonomy": "other",
          "classification.type": "blacklist",
          "classification.identifier": "Suspicious",
          "time.source": "2018-02-13T08:12:00+00:00",
          "feed.name": "Webinspektor"}
EVENT3 = {"raw": utils.base64_encode(REPORT_DATA_SPLIT[120].strip() + REPORT_DATA_SPLIT[122].strip()),
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "https://app.webinspector.com/public/recent_detections",
          "source.url": "http://wapmobi.sextgem.com",
          "classification.taxonomy": "other",
          "classification.identifier": "Suspicious",
          "time.source": "2018-02-13T08:11:46+00:00",
          "classification.type": "blacklist",
          "feed.name": "Webinspektor"}


class TestWebinspektorParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = WebinspektorParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
