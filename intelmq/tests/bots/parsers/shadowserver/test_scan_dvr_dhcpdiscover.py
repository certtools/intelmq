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
                       'testdata/scan_dvr_dhcpdiscover.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible DVR DHCPDiscover',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-scan_dvr_dhcpdiscover-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-dvr-dhcpdiscover',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.alarm_input_channels': 0,
    'extra.alarm_output_channels': 0,
    'extra.amplification': 794.0,
    'extra.device_model': 'BCS-TIP3401IR-E-V',
    'extra.device_serial': '6J0E022PAG35073',
    'extra.device_type': 'IPC',
    'extra.device_vendor': 'General',
    'extra.device_version': '2.800.106F004.0.R',
    'extra.http_port': 80,
    'extra.internal_port': 37777,
    'extra.ipv4_address': '192.168.0.1',
    'extra.ipv4_dhcp_enable': False,
    'extra.ipv4_gateway': '192.168.0.240',
    'extra.ipv4_subnet_mask': '255.255.255.0',
    'extra.ipv6_address': 'fd09:4ab5:dae9:b078::1',
    'extra.ipv6_dhcp_enable': False,
    'extra.ipv6_gateway': 'fd09:4ab5:dae9:b078::ff',
    'extra.ipv6_link_local': 'fe80::3ac4:e8ff:fe03:b3e2/64',
    'extra.mac_address': '38:c4:e8:03:b3:e2',
    'extra.machine_name': '6J0E022PAG35073',
    'extra.manufacturer': 'General',
    'extra.method': 'client.notifyDevInfo',
    'extra.remote_video_input_channels': 0,
    'extra.response_size': 794,
    'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.video_input_channels': 1,
    'extra.video_output_channels': 0,
    'feed.name': 'Accessible DVR DHCPDiscover',
    'protocol.application': 'dvrdhcpdiscover',
    'protocol.transport': 'udp',
    'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 37810,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
   {'__type': 'Event',
    'classification.identifier': 'open-dvr-dhcpdiscover',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.alarm_input_channels': 0,
    'extra.alarm_output_channels': 0,
    'extra.amplification': 761.0,
    'extra.device_model': 'HCVR',
    'extra.device_serial': '2K0488CPAGS0ND6',
    'extra.device_type': 'HCVR',
    'extra.device_vendor': 'Private',
    'extra.device_version': '3.210.1.4',
    'extra.http_port': 80,
    'extra.internal_port': 37777,
    'extra.ipv4_address': '192.168.0.2',
    'extra.ipv4_dhcp_enable': False,
    'extra.ipv4_gateway': '192.168.0.240',
    'extra.ipv4_subnet_mask': '255.255.255.0',
    'extra.ipv6_address': 'fd09:4ab5:dae9:b078::2',
    'extra.ipv6_gateway': 'fd09:4ab5:dae9:b078::ff',
    'extra.ipv6_link_local': 'fe80::3eef:8cff:fe18:a507/64',
    'extra.mac_address': '3c:ef:8c:18:a5:07',
    'extra.machine_name': 'HCVR',
    'extra.manufacturer': 'Private',
    'extra.method': 'client.notifyDevInfo',
    'extra.remote_video_input_channels': 9,
    'extra.response_size': 761,
    'extra.video_input_channels': 3,
    'extra.video_output_channels': 0,
    'feed.name': 'Accessible DVR DHCPDiscover',
    'protocol.application': 'dvrdhcpdiscover',
    'protocol.transport': 'udp',
    'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 37810,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-dvr-dhcpdiscover',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.alarm_input_channels': 0,
    'extra.alarm_output_channels': 0,
    'extra.amplification': 711.0,
    'extra.device_model': 'BCS-XVR0401-IV',
    'extra.device_serial': '5L034FAPAZA0E30',
    'extra.device_type': 'HCVR',
    'extra.device_vendor': 'General',
    'extra.device_version': '4.000.0000002.11',
    'extra.http_port': 80,
    'extra.internal_port': 37777,
    'extra.ipv4_address': '192.168.0.3',
    'extra.ipv4_dhcp_enable': False,
    'extra.ipv4_gateway': '192.168.0.240',
    'extra.ipv4_subnet_mask': '255.255.255.0',
    'extra.ipv6_address': 'fd09:4ab5:dae9:b078::3',
    'extra.ipv6_gateway': 'fd09:4ab5:dae9:b078::ff',
    'extra.ipv6_link_local': 'fe80::3ac4:e8ff:fe02:74da/64',
    'extra.mac_address': '38:c4:e8:02:74:da',
    'extra.machine_name': 'XVR',
    'extra.manufacturer': 'General',
    'extra.method': 'client.notifyDevInfo',
    'extra.remote_video_input_channels': 0,
    'extra.response_size': 711,
    'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.video_input_channels': 4,
    'extra.video_output_channels': 0,
    'feed.name': 'Accessible DVR DHCPDiscover',
    'protocol.application': 'dvrdhcpdiscover',
    'protocol.transport': 'udp',
    'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 37810,
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
