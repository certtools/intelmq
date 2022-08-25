# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_portmapper.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Portmapper',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_portmapper-test-geo.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-portmapper',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 3.7,
    'extra.exports': '/mnt/export 192.168.0.0',
    'extra.programs': '100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; '
                      '100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp;',
    'extra.response_size': 148,
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'portmapper',
    'feed.name': 'Open Portmapper',
    'protocol.application': 'portmapper',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 111,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-portmapper',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 3.7,
    'extra.exports': '/mnt/export 192.168.0.0',
    'extra.programs': '100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; '
                      '100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp;',
    'extra.response_size': 148,
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'portmapper',
    'feed.name': 'Open Portmapper',
    'protocol.application': 'portmapper',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 111,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-portmapper',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 3.7,
    'extra.exports': '/mnt/export 192.168.0.0',
    'extra.programs': '100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp; '
                      '100000 4 111/udp; 100000 3 111/udp; 100000 2 111/udp;',
    'extra.response_size': 148,
    'extra.sector': 'Government',
    'extra.tag': 'portmapper',
    'feed.name': 'Open Portmapper',
    'protocol.application': 'portmapper',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 111,
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
