# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_mdns.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open mDNS',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_mdns-test-geo.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-mdns',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.http_ipv4' : '192.168.0.1',
   'extra.http_ipv6' : 'fd09:4ab5:dae9:b078::1',
   'extra.services' : '_smb._tcp.local.; _device-info._tcp.local.; _http._tcp.local.; _dacp._tcp.local.;',
   'extra.tag' : 'mdns',
   'extra.workstation_ipv4' : '192.168.0.1',
   'extra.workstation_ipv6' : 'fd09:4ab5:dae9:b078::1',
   'feed.name' : 'Open mDNS',
   'protocol.application' : 'mdns',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 5353,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-mdns',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.http_ipv4' : '192.168.0.2',
   'extra.http_ipv6' : 'fd09:4ab5:dae9:b078::2',
   'extra.services' : '_home-assistant._tcp.local.;',
   'extra.tag' : 'mdns',
   'extra.workstation_ipv4' : '192.168.0.2',
   'extra.workstation_ipv6' : 'fd09:4ab5:dae9:b078::2',
   'feed.name' : 'Open mDNS',
   'protocol.application' : 'mdns',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 5353,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-mdns',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.http_info' : '\\\\\"vendor=Synology\\\"\\\" \\\"\\\"model=DS218+\\\"\\\" \\\"\\\"serial=17A0PCN482002\\\"\\\" \\\"\\\"version_major=6\\\"\\\" \\\"\\\"version_minor=2\\\"\\\" \\\"\\\"version_build=25556\\\"\\\" \\\"\\\"admin_port=5000\\\"\\\" \\\"\\\"secure_admin_port=5001\\\"\\\" \\\"\\\"mac_address=00:11:32:80:fd:b5\\\"\\\"\"',
   'extra.http_ipv4' : '192.168.0.3',
   'extra.http_ipv6' : 'fd09:4ab5:dae9:b078::3',
   'extra.http_name' : 'snmeijer.local.',
   'extra.http_port' : 5000,
   'extra.http_ptr' : 'snmeijer._http._tcp.local.',
   'extra.http_target' : 'snmeijer.local.',
   'extra.services' : '_webdav._tcp.local.; _adisk._tcp.local.; _smb._tcp.local.; _http._tcp.local.; _dacp._tcp.local.; _afpovertcp._tcp.local.; _device-info._tcp.local.;',
   'extra.tag' : 'mdns,iot',
   'extra.workstation_ipv4' : '192.168.0.3',
   'extra.workstation_ipv6' : 'fd09:4ab5:dae9:b078::3',
   'feed.name' : 'Open mDNS',
   'protocol.application' : 'mdns',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 5353,
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
