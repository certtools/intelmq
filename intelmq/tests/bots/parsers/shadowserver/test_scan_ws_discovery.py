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
                       'testdata/scan_ws_discovery.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible-WS-Discovery-Service',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-scan_ws_discovery-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-ws-discovery',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 164.83,
    'extra.error': 'Validation constraint violation: SOAP message expected',
    'extra.raw_response': 'c2FtcGxlIHJlc3BvbnNlIGRhdGEK',
    'extra.response_size': 989,
    'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'ws-discovery',
    'feed.name': 'Accessible-WS-Discovery-Service',
    'protocol.application': 'ws-discovery',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 3702,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
   '__type': 'Event',
    'classification.identifier': 'open-ws-discovery',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 183.6,
    'extra.error': 'Validation constraint violation: missing root element',
    'extra.raw_response': 'c2FtcGxlIHJlc3BvbnNlIGRhdGEK',
    'extra.response_size': 918,
    'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'ws-discovery',
    'feed.name': 'Accessible-WS-Discovery-Service',
    'protocol.application': 'ws-discovery',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 3702,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
   '__type': 'Event',
    'classification.identifier': 'open-ws-discovery',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 197.8,
    'extra.error': 'Validation constraint violation: SOAP message expected',
    'extra.raw_response': 'c2FtcGxlIHJlc3BvbnNlIGRhdGEK',
    'extra.response_size': 989,
    'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'ws-discovery',
    'feed.name': 'Accessible-WS-Discovery-Service',
    'protocol.application': 'ws-discovery',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 3702,
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
