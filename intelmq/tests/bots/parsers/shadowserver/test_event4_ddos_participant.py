# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_ddos_participant.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'DDoS Participant',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-event4_ddos_participant-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'ddos-participant',
    'classification.taxonomy': 'availability',
    'classification.type': 'ddos',
    'destination.asn': 65534,
    'destination.geolocation.cc': 'ZZ',
    'destination.geolocation.city': 'City',
    'destination.geolocation.region': 'Region',
    'destination.ip': '172.16.0.1',
    'destination.port': 443,
    'destination.reverse_dns': 'node01.example.net',
    'extra.application': 'https',
    'extra.domain': 'www.example.com',
    'extra.http_method': 'GET',
    'extra.http_path': '/??=GovpfOoaWYlk',
    'feed.name': 'DDoS Participant',
    'malware.name': 'ddos-participant',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 38055,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'ddos-participant',
    'classification.taxonomy': 'availability',
    'classification.type': 'ddos',
    'destination.asn': 65534,
    'destination.geolocation.cc': 'ZZ',
    'destination.geolocation.city': 'City',
    'destination.geolocation.region': 'Region',
    'destination.ip': '172.16.0.2',
    'destination.port': 53,
    'destination.reverse_dns': 'node02.example.net',
    'extra.application': 'dns',
    'feed.name': 'DDoS Participant',
    'malware.name': 'ddos-participant',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 53,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'ddos-participant',
    'classification.taxonomy': 'availability',
    'classification.type': 'ddos',
    'destination.asn': 65534,
    'destination.geolocation.cc': 'ZZ',
    'destination.geolocation.city': 'City',
    'destination.geolocation.region': 'Region',
    'destination.ip': '172.16.0.3',
    'destination.port': 53,
    'destination.reverse_dns': 'node03.example.net',
    'extra.application': 'dns',
    'extra.device_model': 'Exchange',
    'extra.device_type': 'email',
    'extra.device_vendor': 'Microsoft',
    'feed.name': 'DDoS Participant',
    'malware.name': 'ddos-participant',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 53,
    'source.reverse_dns': 'node03.example.com',
    'time.source': '2010-02-10T00:00:02+00:00'
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
