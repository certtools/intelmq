# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_portmapper.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Portmapper',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_portmapper-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open Portmapper',
           "classification.identifier": "open-portmapper",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.programs": "100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; 100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; 100024 1 34213/udp; 100024 1 35984/udp;",
           "extra.tag": "portmapper",
           "protocol.application": "portmapper",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 24961,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "DUSSELDORF",
           "source.geolocation.region": "NORDRHEIN-WESTFALEN",
           "source.ip": "198.51.100.152",
           "source.port": 111,
           "source.reverse_dns": "198-51-100-152.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T04:10:26+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open Portmapper',
           "classification.identifier": "open-portmapper",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.programs": "100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; 100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; 100024 1 33353/udp; 100024 1 42594/udp;",
           "extra.tag": "portmapper",
           "protocol.application": "portmapper",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 24940,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "NUREMBERG",
           "source.geolocation.region": "BAYERN",
           "source.ip": "198.51.100.67",
           "source.port": 111,
           "source.reverse_dns": "198-51-100-67.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T04:10:26+00:00"
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
