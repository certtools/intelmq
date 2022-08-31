# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_memcached.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Memcached',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_memcached-test-geo.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-memcached',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 81.71,
    'extra.curr_connections': 243,
    'extra.pid': 1010,
    'extra.pointer_size': 64,
    'extra.response_size': 1144,
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'memcached',
    'extra.time': '2022-08-21 10:34:06',
    'extra.total_connections': 6106,
    'extra.uptime': 32908114,
    'extra.version': '1.4.15',
    'feed.name': 'Open Memcached',
    'protocol.application': 'memcached',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 50260,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-memcached',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 75.21,
    'extra.curr_connections': 9,
    'extra.pid': 5316,
    'extra.pointer_size': 64,
    'extra.response_size': 1053,
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'memcached',
    'extra.time': '2022-08-21 10:39:21',
    'extra.total_connections': 2962,
    'extra.uptime': 9618498,
    'extra.version': '1.4.13',
    'feed.name': 'Open Memcached',
    'protocol.application': 'memcached',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 11211,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
   {'__type': 'Event',
    'classification.identifier': 'open-memcached',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 31.57,
    'extra.curr_connections': 2,
    'extra.pid': 1460,
    'extra.pointer_size': 32,
    'extra.response_size': 442,
    'extra.tag': 'memcached',
    'extra.time': '2022-08-21 10:39:39',
    'extra.total_connections': 534,
    'extra.uptime': 1375159,
    'extra.version': '1.2.6',
    'feed.name': 'Open Memcached',
    'protocol.application': 'memcached',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 11211,
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
