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
                       'testdata/scan_ssdp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open SSDP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ssdp-test-geo.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-ssdp',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 3.35,
    'extra.cache_control': 'max-age=100',
    'extra.header': 'HTTP/1.1 200 OK',
    'extra.host': 'node01.example.com',
    'extra.location': 'http://192.168.200.254:49152/description.xml',
    'extra.response_size': 325,
    'extra.search_target': 'upnp:rootdevice',
    'extra.sector': 'Government',
    'extra.server': 'Linux/2.6.26, UPnP/1.0, Portable SDK for UPnP devices/1.3.1',
    'extra.systime': 'Sun, 21 Aug 2022 09:51:13 GMT',
    'extra.tag': 'ssdp',
    'extra.unique_service_name': 'uuid:28802880-2880-1880-a880-001bc502f600::upnp:rootdevice',
    'feed.name': 'Open SSDP',
    'protocol.application': 'ssdp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 60194,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-ssdp',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 2.71,
    'extra.cache_control': 'max-age = 1800',
    'extra.header': 'HTTP/1.1 200 OK',
    'extra.host': 'node02.example.com',
    'extra.location': 'http://95.160.216.14:52235/dmr/SamsungMRDesc.xml',
    'extra.response_size': 263,
    'extra.search_target': 'upnp:rootdevice',
    'extra.server': 'Linux/9.0 UPnP/1.0 PROTOTYPE/1.0',
    'extra.tag': 'ssdp',
    'extra.unique_service_name': 'uuid:f144ca92-6816-94b5-b95f-b58180834044::upnp:rootdevice',
    'feed.name': 'Open SSDP',
    'protocol.application': 'ssdp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 38732,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-ssdp',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 4.79,
    'extra.cache_control': 'max-age=1800',
    'extra.header': 'HTTP/1.1 200 OK',
    'extra.host': 'node03.example.com',
    'extra.location': 'http://192.168.1.3:8008/ssdp/device-desc.xml',
    'extra.response_size': 465,
    'extra.search_target': 'upnp:rootdevice',
    'extra.sector': 'Government',
    'extra.server': 'Linux/3.10.79, UPnP/1.0, Portable SDK for UPnP '
                    'devices/1.6.18',
    'extra.systime': 'Sun, 03 Jan 2016 21:37:50 GMT',
    'extra.tag': 'ssdp',
    'extra.unique_service_name': 'uuid:62fa0fc8-079d-d00f-2e22-59b49fb488f9::upnp:rootdevice',
    'feed.name': 'Open SSDP',
    'protocol.application': 'ssdp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 57626,
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
