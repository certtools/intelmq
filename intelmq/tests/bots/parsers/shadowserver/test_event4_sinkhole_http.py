# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_sinkhole_http.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'HTTP Sinkhole IPv4',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_sinkhole_http.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'HTTP Sinkhole IPv4',
           'classification.identifier': 'avalanche-andromeda',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 6939,
           'destination.fqdn': 'differentia.ru',
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'FREMONT',
           'destination.geolocation.region': 'CALIFORNIA',
           'destination.ip': '184.105.1.2',
           'destination.port': 80,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.family': 'andromeda',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 134707,
           'source.geolocation.cc': 'PH',
           'source.geolocation.city': 'DEL PILAR',
           'source.geolocation.region': 'NUEVA ECIJA',
           'source.ip': '103.196.1.2',
           'source.port': 60902,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-03-04T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Sinkhole IPv4',
           'classification.identifier': 'avalanche-andromeda',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 6939,
           'destination.fqdn': 'differentia.ru',
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'FREMONT',
           'destination.geolocation.region': 'CALIFORNIA',
           'destination.ip': '184.105.3.4',
           'destination.port': 80,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.family': 'andromeda',
           'extra.source.naics': 517311,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 8708,
           'source.geolocation.cc': 'RO',
           'source.geolocation.city': 'CONSTANTA',
           'source.geolocation.region': 'CONSTANTA',
           'source.ip': '5.14.3.4',
           'source.port': 55002,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-03-04T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Sinkhole IPv4',
           'classification.identifier': 'avalanche-andromeda',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 6939,
           'destination.fqdn': 'disorderstatus.ru',
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'FREMONT',
           'destination.geolocation.region': 'CALIFORNIA',
           'destination.ip': '184.105.5.6',
           'destination.port': 80,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.source.naics': 517311,
           'extra.family': 'andromeda',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           'source.asn': 9299,
           'source.geolocation.cc': 'PH',
           'source.geolocation.city': 'CEBU',
           'source.geolocation.region': 'CEBU',
           'source.ip': '49.145.5.6',
           'source.port': 31350,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-03-04T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Sinkhole IPv4',
           'classification.identifier': 'avalanche-andromeda',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 6939,
           'destination.fqdn': 'differentia.ru',
           'destination.geolocation.cc': 'US',
           'destination.ip': '184.105.7.8',
           'destination.geolocation.city': 'FREMONT',
           'destination.geolocation.region': 'CALIFORNIA',
           'destination.port': 80,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.source.naics': 517311,
           'extra.family': 'andromeda',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[4]])),
           'source.asn': 8048,
           'source.geolocation.cc': 'VE',
           'source.geolocation.city': 'VALENCIA',
           'source.geolocation.region': 'CARABOBO',
           'source.ip': '200.44.7.8',
           'source.port': 28063,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-03-04T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Sinkhole IPv4',
           'classification.identifier': 'avalanche-andromeda',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 6939,
           'destination.fqdn': 'differentia.ru',
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'FREMONT',
           'destination.geolocation.region': 'CALIFORNIA',
           'destination.ip': '184.105.9.10',
           'destination.port': 80,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.family': 'andromeda',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[5]])),
           'source.asn': 17072,
           'source.geolocation.cc': 'MX',
           'source.geolocation.city': 'JUAREZ',
           'source.geolocation.region': 'CHIHUAHUA',
           'source.ip': '187.189.9.10',
           'source.port': 45335,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-03-04T00:00:00+00:00'}]


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
