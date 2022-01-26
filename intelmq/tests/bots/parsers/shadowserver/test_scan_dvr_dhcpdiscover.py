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
   '__type' : 'Event',
   'classification.identifier' : 'open-dvr-dhcpdiscover',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.alarm_input_channels' : 0,
   'extra.alarm_output_channels' : 0,
   'extra.device_model' : 'HDCVI 1008 - Gerao 2',
   'extra.device_serial' : 'BFBE29078050F',
   'extra.device_type' : 'HDCVI',
   'extra.device_vendor' : 'Intelbras',
   'extra.device_version' : '3.200.24.0',
   'extra.http_port' : 9000,
   'extra.internal_port' : 37777,
   'extra.ipv4_address' : '192.168.0.1',
   'extra.ipv4_dhcp_enable' : False,
   'extra.ipv4_gateway' : '192.168.0.240',
   'extra.ipv4_subnet_mask' : '255.255.255.0',
   'extra.ipv6_address' : 'fd09:4ab5:dae9:b078::1',
   'extra.ipv6_dhcp_enable' : True,
   'extra.ipv6_gateway' : 'fd09:4ab5:dae9:b078::ff',
   'extra.ipv6_link_local' : 'fe80::5a10:8cff:fe19:bffb/64',
   'extra.mac_address' : '58:10:8c:19:bf:fb',
   'extra.machine_name' : 'HDCVI',
   'extra.manufacturer' : 'Intelbras',
   'extra.method' : 'client.notifyDevInfo',
   'extra.remote_video_input_channels' : 2,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.video_input_channels' : 8,
   'extra.video_output_channels' : 0,
   'feed.name' : 'Accessible DVR DHCPDiscover',
   'protocol.application' : 'dvrdhcpdiscover',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 37810,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-dvr-dhcpdiscover',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.alarm_input_channels' : 0,
   'extra.alarm_output_channels' : 0,
   'extra.device_model' : 'MHDX 3116',
   'extra.device_serial' : 'EKHH46019297F',
   'extra.device_type' : 'MHDX',
   'extra.device_vendor' : 'Intelbras',
   'extra.device_version' : '4.000.00IB002.17',
   'extra.http_port' : 80,
   'extra.internal_port' : 37777,
   'extra.ipv4_address' : '192.168.0.2',
   'extra.ipv4_dhcp_enable' : False,
   'extra.ipv4_gateway' : '192.168.0.240',
   'extra.ipv4_subnet_mask' : '255.255.255.0',
   'extra.ipv6_address' : 'fd09:4ab5:dae9:b078::2',
   'extra.ipv6_dhcp_enable' : True,
   'extra.ipv6_gateway' : 'fd09:4ab5:dae9:b078::ff',
   'extra.ipv6_link_local' : 'fe80::26fd:dff:fe55:f232/64',
   'extra.mac_address' : '24:fd:0d:55:f2:32',
   'extra.machine_name' : 'MHDX',
   'extra.manufacturer' : 'Intelbras',
   'extra.method' : 'client.notifyDevInfo',
   'extra.remote_video_input_channels' : 8,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.video_input_channels' : 16,
   'extra.video_output_channels' : 0,
   'feed.name' : 'Accessible DVR DHCPDiscover',
   'protocol.application' : 'dvrdhcpdiscover',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 37810,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-dvr-dhcpdiscover',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.alarm_input_channels' : 0,
   'extra.alarm_output_channels' : 0,
   'extra.device_model' : 'MHDX 5216',
   'extra.device_serial' : 'GMII3200193FP',
   'extra.device_type' : 'MHDX',
   'extra.device_vendor' : 'Intelbras',
   'extra.device_version' : '4.000.00IB002.17',
   'extra.http_port' : 80,
   'extra.internal_port' : 37777,
   'extra.ipv4_address' : '192.168.0.3',
   'extra.ipv4_dhcp_enable' : False,
   'extra.ipv4_gateway' : '192.168.0.240',
   'extra.ipv4_subnet_mask' : '255.255.255.0',
   'extra.ipv6_address' : 'fd09:4ab5:dae9:b078::3',
   'extra.ipv6_dhcp_enable' : True,
   'extra.ipv6_gateway' : 'fd09:4ab5:dae9:b078::ff',
   'extra.ipv6_link_local' : 'fe80::da77:8bff:feb4:92d8/64',
   'extra.mac_address' : 'd8:77:8b:b4:92:d8',
   'extra.machine_name' : 'MHDX',
   'extra.manufacturer' : 'Intelbras',
   'extra.method' : 'client.notifyDevInfo',
   'extra.remote_video_input_channels' : 0,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.video_input_channels' : 16,
   'extra.video_output_channels' : 0,
   'feed.name' : 'Accessible DVR DHCPDiscover',
   'protocol.application' : 'dvrdhcpdiscover',
   'protocol.transport' : 'udp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 37810,
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
