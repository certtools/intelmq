# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_ntp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'NTP Version',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ntp-test-geo.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'ntp-version',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.clk_wander' : 0,
   'extra.clock' : '0xE62E08E9.F0A774D2',
   'extra.frequency' : 0,
   'extra.jitter' : 0,
   'extra.leap' : 3,
   'extra.mintc' : '3',
   'extra.offset' : 0,
   'extra.precision' : -20,
   'extra.refid' : 'INIT',
   'extra.reftime' : '0x00000000.00000000',
   'extra.rootdelay' : 0,
   'extra.rootdispersion' : 0,
   'extra.stratum' : 16,
   'extra.system' : 'UNIX',
   'extra.tag' : 'ntpversion',
   'extra.tc' : 3,
   'extra.version' : '4',
   'feed.name' : 'NTP Version',
   'protocol.application' : 'ntp',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 123,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'ntp-version',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.clk_wander' : 2.64,
   'extra.clock' : '0xe62e0cad.c2ff7c82',
   'extra.frequency' : -11.962,
   'extra.jitter' : 0,
   'extra.leap' : 0,
   'extra.mintc' : '3',
   'extra.offset' : 12.719,
   'extra.precision' : -18,
   'extra.processor' : 'mips64',
   'extra.refid' : '203.248.240.103',
   'extra.reftime' : '0xe62e0be6.60888599',
   'extra.rootdelay' : 6.493,
   'extra.rootdispersion' : 1093.842,
   'extra.stratum' : 3,
   'extra.system' : 'Linux/2.6.38+',
   'extra.tag' : 'ntpversion',
   'extra.tc' : 10,
   'extra.version' : 'ntpd 4.2.8p10@1.3728-o Sun Sep 17 20:40:05 UTC 2017 (1)',
   'feed.name' : 'NTP Version',
   'protocol.application' : 'ntp',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 123,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'ntp-version',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.clock' : '0xE62E0CAD.BCF46BB4',
   'extra.frequency' : 46.122,
   'extra.jitter' : 5.271,
   'extra.leap' : 0,
   'extra.noise' : '0.849',
   'extra.offset' : 3.136,
   'extra.poll' : 10,
   'extra.precision' : -28,
   'extra.refid' : '194.25.7.190',
   'extra.reftime' : '0xE62E08C0.6967CAFB',
   'extra.rootdelay' : 37.173,
   'extra.rootdispersion' : 69.399,
   'extra.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.stability' : '0.028',
   'extra.state' : '4',
   'extra.stratum' : 3,
   'extra.system' : 'UNIX',
   'extra.tag' : 'ntpversion',
   'extra.version' : '4',
   'feed.name' : 'NTP Version',
   'protocol.application' : 'ntp',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 123,
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
