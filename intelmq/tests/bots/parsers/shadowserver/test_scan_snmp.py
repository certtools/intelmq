# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_snmp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open SNMP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_snmp-test-geo.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'open-snmp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.community' : 'public',
   'extra.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'snmp',
   'extra.version' : 2,
   'feed.name' : 'Open SNMP',
   'protocol.application' : 'snmp',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 161,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-snmp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.community' : 'public',
   'extra.device_sector' : 'consumer',
   'extra.device_type' : 'router',
   'extra.device_vendor' : 'MikroTik',
   'extra.sysdesc' : 'RouterOS RB4011iGS+',
   'extra.tag' : 'snmp',
   'extra.version' : 2,
   'feed.name' : 'Open SNMP',
   'protocol.application' : 'snmp',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 161,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-snmp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.community' : 'public',
   'extra.device_model' : 'CG2001-UN2NA',
   'extra.device_sector' : 'consumer',
   'extra.device_type' : 'router',
   'extra.device_vendor' : 'KAONMEDIA',
   'extra.sysdesc' : 'Kaonmedia cablemodem reference design <<HW_REV: v1.0; VENDOR: Kaonmedia; BOOTR: 2.4.0mp1; SW_REV: 3.0.8; MODEL: CG2001-UN2NA>',
   'extra.tag' : 'snmp',
   'extra.version' : 2,
   'feed.name' : 'Open SNMP',
   'protocol.application' : 'snmp',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 161,
   'source.reverse_dns' : 'node03.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:02+00:00'
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
