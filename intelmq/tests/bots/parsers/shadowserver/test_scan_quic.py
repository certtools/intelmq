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
                       'testdata/scan_quic.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible QUIC Report',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_quic-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-quic',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.source.naics' : 517311,
   'extra.tag' : 'quic',
   'extra.version_field_1' : 'Q050',
   'extra.version_field_3' : 'Q046',
   'extra.version_field_4' : 'Q043',
   'feed.name' : 'Accessible QUIC Report',
   'protocol.transport' : 'udp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 5607,
   'source.geolocation.cc' : 'UK',
   'source.geolocation.city' : 'LONDON',
   'source.geolocation.region' : 'LONDON',
   'source.ip' : '176.255.0.0',
   'source.port' : 443,
   'source.reverse_dns' : 'test1.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T14:31:17+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-quic',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.source.naics' : 517311,
   'extra.tag' : 'quic',
   'extra.version_field_1' : 'Q050',
   'extra.version_field_2' : 'Q046',
   'extra.version_field_4' : 'Q043',
   'feed.name' : 'Accessible QUIC Report',
   'protocol.transport' : 'udp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 6327,
   'source.geolocation.cc' : 'CA',
   'source.geolocation.city' : 'MEACHAM',
   'source.geolocation.region' : 'SASKATCHEWAN',
   'source.ip' : '24.244.0.0',
   'source.port' : 443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T14:31:17+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-quic',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.source.naics' : 517919,
   'extra.tag' : 'quic',
   'extra.version_field_2' : 'Q050',
   'extra.version_field_3' : 'Q046',
   'extra.version_field_4' : 'Q043',
   'feed.name' : 'Accessible QUIC Report',
   'protocol.transport' : 'udp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 20940,
   'source.geolocation.cc' : 'JP',
   'source.geolocation.city' : 'OSAKA',
   'source.geolocation.region' : 'OSAKA',
   'source.ip' : '23.60.0.0',
   'source.port' : 443,
   'source.reverse_dns' : 'test3.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T14:31:17+00:00'
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
