# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.blueliv.parser_crimeserver import \
    BluelivCrimeserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'test_parser_crimeserver.data')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()[1:-1]

EXAMPLE_REPORT = {"feed.name": "Blueliv Crimeserver",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-09-02T14:17:58+00:00"
                  }
EXAMPLE_EVENTS = [{
    "__type": "Event",
    "feed.name": "Blueliv Crimeserver",
    "classification.type": "malware",
    "raw": utils.base64_encode(EXAMPLE_LINES[0][:-1]),
    "extra.confidence": 4,
    "extra.time_updated": "2015-12-09T04:45:53+0000",
    "extra.time_first_seen": "2015-10-20T06:14:00+0000",
    "extra.status": "ONLINE",
    "source.url": "http://amirosterweil.weebly.com/uploads/2/3/2/5/23258576/corporate_elearning.pdf",
    "time.source": "2015-12-09T04:43:29+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00",
    "source.geolocation.cc": "US",
    "source.ip": "199.34.228.54"
    }, {
    "__type": "Event",
    "feed.name": "Blueliv Crimeserver",
    "classification.type": "phishing",
    "raw": utils.base64_encode(EXAMPLE_LINES[1][:-1]),
    "extra.status": "ONLINE",
    "extra.time_updated": "2015-12-13T13:55:54+0000",
    "extra.time_first_seen": "2015-07-04T17:08:23+0000",
    "source.url": "http://mondeos-italo.com/store/apple/",
    "time.source": "2015-12-13T13:53:55+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00",
    "source.geolocation.cc": "US",
    }, {
    "__type": "Event",
    "feed.name": "Blueliv Crimeserver",
    "extra.status": "ONLINE",
    "classification.type": "proxy",
    "raw": utils.base64_encode(EXAMPLE_LINES[2]),
    "source.tor_node": True,
    "time.source": "2015-12-13T17:26:23+00:00",
    "time.observation": "2015-12-13T17:26:23+00:00",
    "source.ip": "10.0.0.1"
}]


class TestBluelivCrimeserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BluelivCrimeserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BluelivCrimeserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENTS[0])
        self.assertMessageEqual(1, EXAMPLE_EVENTS[1])
        self.assertMessageEqual(2, EXAMPLE_EVENTS[2])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
