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
                       'testdata/sandbox_conn.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Sandbox Connections',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-sandbox_conn-test.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-conn',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'malware-distribution',
   'destination.fqdn' : 'time.windows.com',
   'feed.name' : 'Sandbox Connections',
   'malware.hash.md5' : 'b575ce6dcce6502a8431db5610135c25',
   'protocol.transport' : 'udp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 8075,
   'source.geolocation.cc' : 'US',
   'source.ip' : '40.119.6.228',
   'source.port' : 123,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:00:03+00:00'
},
        {
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-conn',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'malware-distribution',
   'feed.name' : 'Sandbox Connections',
   'malware.hash.md5' : 'c0d947f9a8685b0d9f3efdba966389c2',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 3356,
   'source.geolocation.cc' : 'US',
   'source.ip' : '8.252.70.126',
   'source.port' : 80,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:00:03+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-conn',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'malware-distribution',
   'feed.name' : 'Sandbox Connections',
   'malware.hash.md5' : 'c0d947f9a8685b0d9f3efdba966389c2',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 8075,
   'source.geolocation.cc' : 'US',
   'source.ip' : '52.109.8.22',
   'source.port' : 443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:00:03+00:00'
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
