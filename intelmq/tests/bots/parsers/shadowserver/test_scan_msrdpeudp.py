# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_msrdpeudp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible MS RDPEUDP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_msrdpeudp-test-geo.csv",
                  }

EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible MS RDPEUDP',
           "classification.identifier": "accessible-msrdpeudp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.naics": 518210,
           "extra.sessionid": "05d459c3",
           "extra.tag": "rdpeudp",
           "protocol.transport": "udp",
           "raw": utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 20473,
           "source.geolocation.cc": "US",
           "source.geolocation.city": "ELK GROVE VILLAGE",
           "source.geolocation.region": "ILLINOIS",
           "source.ip": "198.51.100.39",
           "source.port": 3389,
           "source.reverse_dns": "198-51-100-39.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2021-01-20T13:18:51+00:00",
           },
           {'__type': 'Event',
           'feed.name': 'Accessible MS RDPEUDP',
           "classification.identifier": "accessible-msrdpeudp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.naics": 518210,
           "extra.sessionid": "055f5d9a",
           "extra.tag": "rdpeudp",
           "protocol.transport": "udp",
           "raw": utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 38365,
           "source.geolocation.cc": "CN",
           "source.geolocation.city": "LISHUI",
           "source.geolocation.region": "ZHEJIANG SHENG",
           "source.ip": "198.51.100.141",
           "source.port": 1234,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2021-01-20T13:18:52+00:00",
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
