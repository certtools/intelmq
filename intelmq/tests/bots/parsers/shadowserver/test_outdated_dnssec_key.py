# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/outdated_dnssec_key.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Outdated DNSSEC Key",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-outdated_dnssec_key-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'outdated-dnssec-key',
           'classification.taxonomy': 'availability',
           'classification.type': 'other',
           'destination.asn': 65537,
           'destination.geolocation.cc': 'US',
           'destination.ip': '10.10.10.11',
           'destination.port': 53,
           'extra.destination.sector': 'Information Technology',
           'extra.public_source': 'verisign',
           'extra.sector': 'Information Technology',
           'extra.tag': 'outdated-dnssec-key',
           'feed.name': 'ShadowServer Outdated DNSSEC Key',
           'protocol.application': 'dns',
           'protocol.transport': 'udp',
           'source.asn': 65536,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '10.10.10.10',
           'source.reverse_dns': 'example.com',
           'time.source': '2018-10-18T00:03:50+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
           },
          {'__type': 'Event',
           'classification.identifier': 'outdated-dnssec-key',
           'classification.taxonomy': 'availability',
           'classification.type': 'other',
           'destination.asn': 65537,
           'destination.geolocation.cc': 'US',
           'destination.ip': 'fe80::2',
           'destination.port': 53,
           'extra.public_source': 'verisign',
           'extra.tag': 'outdated-dnssec-key',
           'feed.name': 'ShadowServer Outdated DNSSEC Key',
           'protocol.application': 'dns',
           'protocol.transport': 'udp',
           'source.asn': 65536,
           'source.geolocation.cc': 'AT',
           'source.ip': 'fe80::1',
           'source.reverse_dns': 'example.com',
           'time.source': '2018-10-18T05:08:36+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
           }
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
