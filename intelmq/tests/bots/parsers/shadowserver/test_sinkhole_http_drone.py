# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
          'testdata/sinkhole_http_drone.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Sinkhole HTTP Drone',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-sinkhole_http_drone-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Sinkhole HTTP Drone',
           "classification.taxonomy": "malicious code",
           "classification.type": "infected-system",
           "destination.asn": 393667,
           "destination.geolocation.cc": "US",
           "destination.ip": "198.51.100.182",
           "destination.port": 80,
           "destination.url": "http://198.51.100.68/search?q=0",
           "extra.naics": 518210,
           "extra.sic": 737415,
           "extra.user_agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
           "malware.name": "downadup",
           "protocol.application": "http",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 6830,
           "source.geolocation.cc": "AT",
           "source.ip": "198.51.100.6",
           "source.port": 49121,
           "source.reverse_dns": "198-51-100-6.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2018-03-21T00:00:07+00:00"
           },
          {'__type': 'Event',
           'feed.name': 'Sinkhole HTTP Drone',
           "classification.taxonomy": "malicious code",
           "classification.type": "infected-system",
           "destination.asn": 6939,
           "destination.fqdn": "198-51-100-74.example.net",
           "destination.geolocation.cc": "US",
           "destination.ip": "198.51.100.35",
           "destination.port": 80,
           "malware.name": "avalanche-goznym",
           "protocol.application": "http",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 8447,
           "source.geolocation.cc": "AT",
           "source.ip": "198.51.100.74",
           "source.port": 28113,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2018-03-21T00:00:12+00:00"
           },
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
