# SPDX-FileCopyrightText: 2020 Thomas Hungenberg
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_coap.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible-CoAP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2020-06-29T00:00:00+00:00",
                  "extra.file_name": "2020-06-28-scan_coap-test-geo.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'accessible-coap',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 2.05,
    'extra.response': '</api>,</api/v1>,</.well-known/core>',
    'extra.response_size': 43,
    'extra.tag': 'coap',
    'extra.version': '2',
    'feed.name': 'Accessible-CoAP',
    'protocol.application': 'coap',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 5683,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-coap',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 5.38,
    'extra.response': '</fw>,</efento>,</efento/c>,</efento/i>,</efento/m>,</efento/t>,</sw>,</api>,</api/v1>,</.well-known/core>',
    'extra.response_size': 113,
    'extra.tag': 'coap',
    'extra.version': '2',
    'feed.name': 'Accessible-CoAP',
    'protocol.application': 'coap',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 5683,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-coap',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 113.5,
    'extra.response': '`EsjAy************************************************************|CoAP '
                      'RFC 7252                                               '
                      '|************************************************************|This '
                      'server is using the Eclipse Californium (Cf) CoAP '
                      'framework|published under EPL+EDL: '
                      'http://www.eclipse.org/californium/||(c) 2014, 2015, 2016 '
                      'Institute for Pervasive Computing, ETH Zurich and '
                      'others|************************************************************',
    'extra.response_size': 454,
    'extra.tag': 'coap',
    'extra.version': '1',
    'feed.name': 'Accessible-CoAP',
    'protocol.application': 'coap',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 5683,
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
