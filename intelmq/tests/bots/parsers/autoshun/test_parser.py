# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.autoshun.parser import AutoshunParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'shunlist.html')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Autoshun",
                  "feed.url": "https://www.autoshun.org/files/shunlist.html",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-09-02T14:17:58+00:00"
                  }
EXAMPLE_EVENT0 = {
    "__type": "Event",
    "feed.name": "Autoshun",
    "classification.type": "scanner",
    "feed.url": "https://www.autoshun.org/files/shunlist.html",
    "raw": "PHRyPjx0ZD4xOTguNTEuMTAwLjQ1PC90ZD48dGQ+MjAxNi0wNS0xNyAxMDo1OToyNzwvdGQ+PHRkPlJBIFNDQU4gVW51c3VhbGx5IGZhc3QgVGVybWluYWwgU2VydmVyIFRyYWZmaWMgSW5ib3VuZDwvdGQ+PC90cj4=",
    "event_description.text": "RA SCAN Unusually fast Terminal Server Traffic Inbound",
    "time.source": "2016-05-17T15:59:27+00:00",
    "time.observation": "2015-05-17T14:17:5810:59:27+00:00",
    "source.ip": "198.51.100.45"
}
EXAMPLE_EVENT1 = {
    "__type": "Event",
    "feed.name": "Autoshun",
    "classification.type": "unknown",
    "feed.url": "https://www.autoshun.org/files/shunlist.html",
    "raw": "PHRyPjx0ZD4xOTguNTEuMTAwLjg2PC90ZD48dGQ+MjAxNi0wNS0xOCAxNDowMTowNjwvdGQ+PHRkPk1TIFRlcm1pbmFsIFNlcnZlciBTaW5nbGUgQ2hhcmFjdGVyIExvZ2luLCBwb3NzaWJsZSBNb3J0byBpbmJvdW5kPC90ZD48L3RyPg==",
    "event_description.text": "MS Terminal Server Single Character Login, possible Morto inbound",
    "time.source": "2016-05-18T19:01:06+00:00",
    "time.observation": "2015-05-17T14:17:5810:59:27+00:00",
    "source.ip": "198.51.100.86"
}


class TestAutoshunParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AutoshunParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AutoshunParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT0)
        self.assertMessageEqual(1, EXAMPLE_EVENT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
