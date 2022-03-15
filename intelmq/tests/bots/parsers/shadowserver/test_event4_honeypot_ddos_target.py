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
                       'testdata/event4_honeypot_ddos_target.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Honeypot DDoS Target Events',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-event4_honeypot_ddos_target-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'honeypot-ddos-target',
   'classification.taxonomy' : 'availability',
   'classification.type' : 'ddos',
   'destination.asn' : 65534,
   'destination.geolocation.cc' : 'ZZ',
   'destination.geolocation.city' : 'City',
   'destination.geolocation.region' : 'Region',
   'destination.ip' : '172.16.0.1',
   'destination.port' : 80,
   'destination.reverse_dns' : 'node01.example.net',
   'extra.application' : 'mirai',
   'extra.attack' : 'atk0',
   'extra.dst_netmask' : '32',
   'extra.dst_network' : '115.238.198.85/32',
   'extra.duration' : 30,
   'extra.family' : 'mirai',
   'extra.packet_length' : 1440,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'mirai',
   'feed.name' : 'Honeypot DDoS Target Events',
   'malware.name' : 'ddos',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 61234,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'honeypot-ddos-target',
   'classification.taxonomy' : 'availability',
   'classification.type' : 'ddos',
   'destination.asn' : 65534,
   'destination.geolocation.cc' : 'ZZ',
   'destination.geolocation.city' : 'City',
   'destination.geolocation.region' : 'Region',
   'destination.ip' : '172.16.0.2',
   'destination.port' : 43437,
   'destination.reverse_dns' : 'node02.example.net',
   'extra.application' : 'mirai',
   'extra.attack' : 'atk0',
   'extra.destination.sector' : 'Information',
   'extra.dst_netmask' : '32',
   'extra.dst_network' : '52.184.50.250/32',
   'extra.duration' : 30,
   'extra.family' : 'mirai',
   'extra.packet_length' : 1440,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'mirai',
   'feed.name' : 'Honeypot DDoS Target Events',
   'malware.name' : 'ddos',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 61234,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'honeypot-ddos-target',
   'classification.taxonomy' : 'availability',
   'classification.type' : 'ddos',
   'destination.asn' : 65534,
   'destination.geolocation.cc' : 'ZZ',
   'destination.geolocation.city' : 'City',
   'destination.geolocation.region' : 'Region',
   'destination.ip' : '172.16.0.3',
   'destination.port' : 80,
   'destination.reverse_dns' : 'node03.example.net',
   'extra.application' : 'mirai',
   'extra.attack' : 'atk10',
   'extra.dst_netmask' : '32',
   'extra.dst_network' : '211.99.102.216/32',
   'extra.duration' : 30,
   'extra.family' : 'mirai',
   'extra.packet_length' : 1440,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'mirai',
   'feed.name' : 'Honeypot DDoS Target Events',
   'malware.name' : 'ddos',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 61234,
   'source.reverse_dns' : 'node03.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
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
