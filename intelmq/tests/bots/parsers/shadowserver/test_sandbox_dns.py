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
   'extra.type' : 'A',
   'feed.name' : 'Sandbox DNS',
   'malware.hash.md5' : 'b575ce6dcce6502a8431db5610135c25',
   'protocol.application' : 'dns',
   'raw' : 'InRpbWVzdGFtcCIsIm1kNWhhc2giLCJyZXF1ZXN0IiwidHlwZSIsInJlc3BvbnNlIiwiZmFtaWx5IiwidGFnIiwic291cmNlIgoiMjAyMi0wMS0xMCAwMDowMDowMiIsImI1NzVjZTZkY2NlNjUwMmE4NDMxZGI1NjEwMTM1YzI1IiwidGltZS53aW5kb3dzLmNvbSIsIkEiLCI0MC4xMTkuNi4yMjgiLCws',
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
   'extra.type' : 'A',
   'feed.name' : 'Sandbox DNS',
   'malware.hash.md5' : '807679198a39c80d3ca07e60fd51b581',
   'protocol.application' : 'dns',
   'raw' : 'InRpbWVzdGFtcCIsIm1kNWhhc2giLCJyZXF1ZXN0IiwidHlwZSIsInJlc3BvbnNlIiwiZmFtaWx5IiwidGFnIiwic291cmNlIgoiMjAyMi0wMS0xMCAwMDowMDowOCIsIjgwNzY3OTE5OGEzOWM4MGQzY2EwN2U2MGZkNTFiNTgxIiwidGltZS53aW5kb3dzLmNvbSIsIkEiLCI0MC4xMTkuNi4yMjgiLCws',
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
   'extra.type' : 'A',
   'feed.name' : 'Sandbox DNS',
   'malware.hash.md5' : 'd97e973b9bf073bd3a217425259cea26',
   'protocol.application' : 'dns',
   'raw' : 'InRpbWVzdGFtcCIsIm1kNWhhc2giLCJyZXF1ZXN0IiwidHlwZSIsInJlc3BvbnNlIiwiZmFtaWx5IiwidGFnIiwic291cmNlIgoiMjAyMi0wMS0xMCAwMDowMDoyMCIsImQ5N2U5NzNiOWJmMDczYmQzYTIxNzQyNTI1OWNlYTI2IiwiY2xpZW50LW9mZmljZTM2NS10YXMubXNlZGdlLm5ldCIsIkEiLCIxMy4xMDcuNS44OCIsLCw=',
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
