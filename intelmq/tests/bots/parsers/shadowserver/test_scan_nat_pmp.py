# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_nat_pmp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open NATPMP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_nat_pmp-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open NATPMP',
           "classification.identifier": "open-natpmp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.external_ip": "198.51.100.66",
           "extra.opcode": "128",
           "extra.tag": "nat-pmp",
           "extra.uptime": "246698",
           "protocol.application": "natpmp",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 31334,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "AUGSBURG",
           "source.geolocation.region": "BAYERN",
           "source.ip": "198.51.100.50",
           "source.port": 5351,
           "source.reverse_dns": "198-51-100-50.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T05:08:45+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open NATPMP',
           "classification.identifier": "open-natpmp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.external_ip": "198.51.100.156",
           "extra.opcode": "128",
           "extra.tag": "nat-pmp",
           "extra.uptime": "47483",
           "protocol.application": "natpmp",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 9066,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "GEISA",
           "source.geolocation.region": "THURINGEN",
           "source.ip": "198.51.100.139",
           "source.port": 5351,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T05:08:45+00:00"
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
