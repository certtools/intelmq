# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/ddos_amplification.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Amplification DDoS Victim',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-ddos_amplification-test-test.csv"
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Amplification DDoS Victim',
           'classification.identifier': 'amplification-ddos-victim',
           'classification.taxonomy': 'availability',
           'classification.type': 'ddos',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2019-01-01T00:00:00+00:00',
           'time.source': '2018-10-09T06:00:06+00:00',
           'source.ip': '192.0.2.10',
           'source.port': 53,
           'protocol.transport': 'udp',
           'destination.port': 13,
           'source.reverse_dns': '192-0-2-10.example.net',
           'source.asn': 44395,
           'source.geolocation.cc': 'AM',
           'source.geolocation.region': 'YEREVAN',
           'source.geolocation.city': 'YEREVAN',
           'extra.tag': 'daytime',
           'extra.request': 'DAYTIME Request',
           'extra.count': 15,
           'extra.bytes': 2220,
           'extra.sensor_geo': 'RU',
           'extra.sector': 'IT1',
           'extra.end_time': '2018-10-09 06:10:01',
           'extra.public_source': 'SSS',
           },
           {'__type': 'Event',
           'feed.name': 'Amplification DDoS Victim',
           'classification.identifier': 'amplification-ddos-victim',
           'classification.taxonomy': 'availability',
           'classification.type': 'ddos',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': '2019-01-01T00:00:00+00:00',
           'time.source': '2018-10-09T08:14:37+00:00',
           'source.ip': '192.0.2.50',
           'source.port': 53,
           'protocol.transport': 'udp',
           'destination.port': 123,
           'source.reverse_dns': 'dhcp-50-2-0-192.net1.bg',
           'source.asn': 43561,
           'source.geolocation.cc': 'BG',
           'source.geolocation.region': 'SOFIA-GRAD',
           'source.geolocation.city': 'SOFIA',
           'extra.tag': 'ntp',
           'extra.request': 'Standard query response 0xe98a  NS auth111.ns.uu.net NS auth120.ns.uu.net',
           'extra.count': 15,
           'extra.bytes': 2700,
           'extra.sensor_geo': 'RU',
           'extra.sector': 'IT2',
           'extra.end_time': '2018-10-09 10:14:59',
           'extra.public_source': 'SSS',
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
