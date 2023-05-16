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
                       'testdata/scan_stun.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible-Session-Traversal-Utilities-for-NAT',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-scan_stun-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-stun',
    'classification.taxonomy': 'other',
    'classification.type': 'other',
    'extra.amplification': 5.4,
    'extra.fingerprint': '0xfaedd06e',
    'extra.magic_cookie': '2112a442',
    'extra.mapped_address': '192.168.0.1',
    'extra.mapped_family': '01',
    'extra.mapped_port': 3243,
    'extra.message_length': 88,
    'extra.message_type': '0101',
    'extra.response_size': 108,
    'extra.software': "Coturn-4.5.1.1 'dan Eider'",
    'extra.tag': 'stun',
    'extra.transaction_id': '000000000000000000000000',
    'extra.xor_mapped_address': '192.168.0.1',
    'extra.xor_mapped_family': '01',
    'extra.xor_mapped_port': 3243,
    'feed.name': 'Accessible-Session-Traversal-Utilities-for-NAT',
    'protocol.application': 'session traversal utilities for nat',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 3478,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-stun',
    'classification.taxonomy': 'other',
    'classification.type': 'other',
    'extra.amplification': 5.4,
    'extra.fingerprint': '0x21128641',
    'extra.magic_cookie': '2112a442',
    'extra.mapped_address': '51.77.39.195',
    'extra.mapped_family': '01',
    'extra.mapped_port': 45877,
    'extra.message_length': 88,
    'extra.message_type': '0101',
    'extra.response_size': 108,
    'extra.software': "Coturn-4.5.1.1 'dan Eider'",
    'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'stun',
    'extra.transaction_id': '000000000000000000000000',
    'extra.xor_mapped_address': '192.168.0.2',
    'extra.xor_mapped_family': '01',
    'extra.xor_mapped_port': 45877,
    'feed.name': 'Accessible-Session-Traversal-Utilities-for-NAT',
    'protocol.application': 'session traversal utilities for nat',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 3478,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-stun',
    'classification.taxonomy': 'other',
    'classification.type': 'other',
    'extra.amplification': 4.8,
    'extra.magic_cookie': '2112a442',
    'extra.mapped_address': '192.168.0.3',
    'extra.mapped_family': '01',
    'extra.mapped_port': 16321,
    'extra.message_length': 76,
    'extra.message_type': '0101',
    'extra.response_size': 96,
    'extra.software': "ApolloProxy-1.20.1.28 'sunflower'",
    'extra.tag': 'stun',
    'extra.transaction_id': '000000000000000000000000',
    'extra.xor_mapped_address': '188.68.240.32',
    'extra.xor_mapped_family': '01',
    'extra.xor_mapped_port': 16321,
    'feed.name': 'Accessible-Session-Traversal-Utilities-for-NAT',
    'protocol.application': 'session traversal utilities for nat',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 3478,
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
