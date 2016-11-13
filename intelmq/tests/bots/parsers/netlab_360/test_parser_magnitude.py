# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.netlab_360.parser_magnitude import Netlab360MagnitudeParserBot

with open(os.path.join(os.path.dirname(__file__), 'magnitude.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Netlab 360 Magnitude",
                  "feed.url": "http://data.netlab.360.com/feeds/ek/magnitude.txt",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "report",
                  "time.observation": "2016-01-01T00:00:00+00:00",
                 }
EVENTS = [{"feed.name": "Netlab 360 Magnitude",
           "feed.url": "http://data.netlab.360.com/feeds/ek/magnitude.txt",
           "__type": "Event",
           "time.source": "2016-11-12T10:31:05+00:00",
           "destination.fqdn": "3ebo08o4ct0f6n2336.insides.party",
           "destination.ip": "178.32.227.12",
           "destination.url": "http://3ebo08o4ct0f6n2336.insides.party/d97cc5cfab47e305536690a9987115ac",
           "classification.type": "exploit",
           "time.observation": "2016-01-01T00:00:00+00:00",
           "event_description.text": "magnitude",
           "event_description.url": "http://data.netlab.360.com/ek",
           "raw": "TWFnbml0dWRlCTE0Nzg5NDY2NjUJMTc4LjMyLjIyNy4xMgkzZWJvMDhvNGN0MGY2bjIzMzYuaW5zaWRlcy5wYXJ0eQlodHRwOi8vM2VibzA4bzRjdDBmNm4yMzM2Lmluc2lkZXMucGFydHkvZDk3Y2M1Y2ZhYjQ3ZTMwNTUzNjY5MGE5OTg3MTE1YWM=",
          }]

class TestNetlab360MagnitudeParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Netlab360MagnitudeParserBot
    """
    @classmethod
    def set_bot(cls):
        cls.bot_reference = Netlab360MagnitudeParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])

if __name__ == '__main__':
    unittest.main()
