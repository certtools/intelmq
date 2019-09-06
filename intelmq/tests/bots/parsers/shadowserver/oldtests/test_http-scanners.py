# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'http-scanners.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer HTTP-Scanners",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer HTTP-Scanners',
           'feed.name': 'ShadowServer HTTP-Scanners',
           'classification.identifier': 'http',
           'classification.taxonomy': 'information gathering',
           'classification.type': 'scanner',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2019-01-01T00:00:00+00:00',
           'time.source': '2018-08-29T00:00:05+00:00',
           'source.ip': '198.51.100.5',
           'source.port': 52513,
           'source.asn': 27668,
           'source.geolocation.cc': 'EC',
           'source.geolocation.region': 'AZUAY',
           'source.geolocation.city': 'CUENCA',
           'source.reverse_dns': '198-51-100-5.example.net',
           'destination.ip': '203.0.113.6',
           'destination.port': 80,
           'destination.asn': 17169,
           'destination.geolocation.cc': 'AT',
           'destination.fqdn': '203-0-113-6.example.net',
           'extra.type': 'http-scan',
           'extra.naics': 1,
           'extra.sic': 2,
           'extra.sector': 'IT1',
           'extra.destination.sector': 'IT2',
           'extra.public_source': 'SISSDEN',
           'extra.sensorid': '53c1549f-f806-4b82-8b3a-6673456cd40f',
           'extra.pattern': 'example-pattern',
           'extra.url': '/',
           'extra.file.md5': '12345',
           'extra.file.sha256': '67890',
           'extra.request_raw': 'GET / HTTP/1.1',
           },
           {'__type': 'Event',
           'feed.name': 'ShadowServer HTTP-Scanners',
           'feed.name': 'ShadowServer HTTP-Scanners',
           'classification.identifier': 'http',
           'classification.taxonomy': 'information gathering',
           'classification.type': 'scanner',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': '2019-01-01T00:00:00+00:00',
           'time.source': '2018-08-29T00:04:08+00:00',
           'source.ip': '198.51.100.3',
           'source.port': 33418,
           'source.asn': 23033,
           'source.geolocation.cc': 'US',
           'source.geolocation.region': 'WASHINGTON',
           'source.geolocation.city': 'EVERETT',
           'source.reverse_dns': '198-51-100-3.example.net',
           'destination.ip': '203.0.113.217',
           'destination.port': 80,
           'destination.asn': 56630,
           'destination.geolocation.cc': 'RU',
           'destination.fqdn': '203-0-113-217.example.net',
           'extra.type': 'http-scan',
           'extra.naics': 1,
           'extra.sic': 2,
           'extra.sector': 'Communications',
           'extra.destination.sector': 'IT',
           'extra.public_source': 'SISSDEN',
           'extra.sensorid': '5800ff5d-277e-48aa-b904-0997a00c6a37',
           'extra.pattern': 'example-pattern',
           'extra.url': '/axis-cgi/aol%2A/_do/rss_popup?blogID=',
           'extra.file.md5': '09876',
           'extra.file.sha256': '54321',
           'extra.request_raw': 'GET /axis-cgi/aol%2A/_do/rss_popup?blogID= HTTP/1.1',
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
        cls.sysconfig = {'feedname': 'HTTP-Scanners'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
