# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_xdmcp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer XDMCP",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_xdmcp-test-geo.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-xdmcp',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 6.29,
    'extra.opcode': 'Willing',
    'extra.reported_hostname': 'node01.example.com',
    'extra.size': 44,
    'extra.status': 'Linux 3.0.101-100-default',
    'extra.tag': 'xdmcp',
    'feed.name': 'ShadowServer XDMCP',
    'protocol.application': 'xdmcp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 177,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-xdmcp',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 6.86,
    'extra.opcode': 'Willing',
    'extra.reported_hostname': 'node02.example.com',
    'extra.size': 48,
    'extra.status': 'Linux 2.6.9-103.ELsmp',
    'extra.tag': 'xdmcp',
    'feed.name': 'ShadowServer XDMCP',
    'protocol.application': 'xdmcp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 47074,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-xdmcp',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 6.57,
    'extra.opcode': 'Willing',
    'extra.reported_hostname': 'node03.example.com',
    'extra.size': 46,
    'extra.status': '1 user,  load: 6,5, 6,6, 6,6',
    'extra.tag': 'xdmcp',
    'feed.name': 'ShadowServer XDMCP',
    'protocol.application': 'xdmcp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 177,
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
