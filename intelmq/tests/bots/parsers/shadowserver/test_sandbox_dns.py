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
                       'testdata/sandbox_dns.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Sandbox DNS',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-sandbox_dns-test.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-dns',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.request' : 'time.windows.com',
   'extra.response' : '40.119.6.228',
   'extra.dns_query_type' : 'A',
   'feed.name' : 'Sandbox DNS',
   'malware.hash.md5' : 'b575ce6dcce6502a8431db5610135c25',
   'protocol.application' : 'dns',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:00:02+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-dns',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.request' : 'time.windows.com',
   'extra.response' : '40.119.6.228',
   'extra.dns_query_type' : 'A',
   'feed.name' : 'Sandbox DNS',
   'malware.hash.md5' : '807679198a39c80d3ca07e60fd51b581',
   'protocol.application' : 'dns',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:00:08+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-dns',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.request' : 'client-office365-tas.msedge.net',
   'extra.response' : '13.107.5.88',
   'extra.dns_query_type' : 'A',
   'feed.name' : 'Sandbox DNS',
   'malware.hash.md5' : 'd97e973b9bf073bd3a217425259cea26',
   'protocol.application' : 'dns',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:00:20+00:00'
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
