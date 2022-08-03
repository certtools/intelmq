# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/device_id.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Device ID',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-device_id-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'device-id',
   'classification.taxonomy' : 'other',
   'classification.type' : 'undetermined',
   'extra.device_model' : 'FortiGate',
   'extra.device_type' : 'firewall',
   'extra.device_vendor' : 'Fortinet',
   'extra.naics' : 517311,
   'feed.name' : 'Device ID',
   'extra.tag' : 'ssl,vpn',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 2116,
   'source.geolocation.cc' : 'NO',
   'source.geolocation.city' : 'TROMVIK',
   'source.geolocation.region' : 'TROMS OG FINNMARK',
   'source.ip' : '88.84.0.0',
   'source.port' : 10443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'device-id',
   'classification.taxonomy' : 'other',
   'classification.type' : 'undetermined',
   'extra.device_model' : 'FortiGate',
   'extra.device_type' : 'firewall',
   'extra.device_vendor' : 'Fortinet',
   'feed.name' : 'Device ID',
   'extra.tag' : 'ssl,vpn',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 27843,
   'source.geolocation.cc' : 'PE',
   'source.geolocation.city' : 'LIMA',
   'source.geolocation.region' : 'METROPOLITANA DE LIMA',
   'source.ip' : '170.231.0.0',
   'source.port' : 10443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'device-id',
   'classification.taxonomy' : 'other',
   'classification.type' : 'undetermined',
   'extra.device_model' : 'FortiGate',
   'extra.device_type' : 'firewall',
   'extra.device_vendor' : 'Fortinet',
   'extra.naics' : 517311,
   'feed.name' : 'Device ID',
   'extra.tag' : 'ssl,vpn',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 4181,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'MILWAUKEE',
   'source.geolocation.region' : 'WISCONSIN',
   'source.ip' : '96.60.0.0',
   'source.port' : 10443,
   'source.reverse_dns' : '96-60-66-218.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
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
