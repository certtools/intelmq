# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/sinkhole_dns.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Sinkhole DNS",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-sinkhole_dns-test-geo.csv",
                  }

EVENTS = [{"__type": "Event",
           "feed.name": "Sinkhole DNS",
           "classification.identifier": "sinkholedns",
           "classification.taxonomy": "other",
           "classification.type": "other",
           "extra.naics": 0,
           "extra.tag": "boaxxe",
           "extra.count": 1,
           "extra.dns_query": '4.wiNsrw.Com',
           "extra.response": "",
           "extra.sector": "",
           "extra.dns_query_type": "A",
           "raw": utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 25192,
           "source.geolocation.cc": "CZ",
           "source.geolocation.region": "PRAHA",
           "source.ip": "198.51.100.1",
           "source.port": 40159,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2020-12-21T00:00:00+00:00",
           "protocol.application": "dns",
           },
           {'__type': 'Event',
           "feed.name": 'Sinkhole DNS',
           "classification.identifier": "sinkholedns",
           "classification.taxonomy": "other",
           "classification.type": "other",
           "extra.naics": 0,
           "extra.tag": "tsifiri",
           "extra.count": 1,
           "extra.dns_query": "198-51-100-81.example.net",
           "extra.response": "",
           "extra.sector": "Communications",
           "extra.dns_query_type": "A",
           "raw": utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 38044,
           "source.geolocation.cc": "MY",
           "source.geolocation.region": "SABAH",
           "source.ip": "198.51.100.81",
           "source.port": 62937,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2020-12-21T00:00:06+00:00",
           "protocol.application": "dns",
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
