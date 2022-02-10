# SPDX-FileCopyrightText: 2021 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/event4_sinkhole_dns.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Sinkhole DNS",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_sinkhole_dns-test-geo.csv",
                  }

EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'sinkhole-dns',
   'extra.tag' : 'msexchange',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.count' : '1',
   'extra.infection' : 'calypso',
   'extra.query' : 'YolkIsh.COM',
   'extra.query_type' : 'A',
   'extra.source.naics' : 518210,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'feed.name' : 'Sinkhole DNS',
   'malware.name' : 'calypso',
   'protocol.application' : 'dns',
   'protocol.transport' : 'udp',
   'raw' : 'InRpbWVzdGFtcCIsInByb3RvY29sIiwic3JjX2lwIiwic3JjX3BvcnQiLCJzcmNfYXNuIiwic3JjX2dlbyIsInNyY19yZWdpb24iLCJzcmNfY2l0eSIsInNyY19ob3N0bmFtZSIsInNyY19uYWljcyIsInNyY19zZWN0b3IiLCJkZXZpY2VfdmVuZG9yIiwiZGV2aWNlX3R5cGUiLCJkZXZpY2VfbW9kZWwiLCJpbmZlY3Rpb24iLCJmYW1pbHkiLCJ0YWciLCJxdWVyeV90eXBlIiwicXVlcnkiLCJjb3VudCIKIjIwMjItMDEtMDYgMDA6MDA6MDIiLCJ1ZHAiLCIyMTcuMTEwLjAuMCIsMjk2MTQsODIyMCwiREUiLCJIRVNTRU4iLCJGUkFOS0ZVUlQgQU0gTUFJTiIsLDUxODIxMCwiQ29tbXVuaWNhdGlvbnMsIFNlcnZpY2UgUHJvdmlkZXIsIGFuZCBIb3N0aW5nIFNlcnZpY2UiLCwsLCJjYWx5cHNvIiwiY2FseXBzbyIsIm1zZXhjaGFuZ2UiLCJBIiwiWW9sa0lzaC5DT00iLDE=',
   'source.asn' : 8220,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'FRANKFURT AM MAIN',
   'source.geolocation.region' : 'HESSEN',
   'source.ip' : '217.110.0.0',
   'source.port' : 29614,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-01-06T00:00:02+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'sinkhole-dns',
   'extra.tag' : 'rat',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.count' : '1',
   'extra.infection' : 'orcus',
   'extra.query' : 'verble.rocks',
   'extra.query_type' : 'A',
   'extra.source.naics' : 518210,
   'feed.name' : 'Sinkhole DNS',
   'malware.name' : 'orcus',
   'protocol.application' : 'dns',
   'protocol.transport' : 'udp',
   'raw' : 'InRpbWVzdGFtcCIsInByb3RvY29sIiwic3JjX2lwIiwic3JjX3BvcnQiLCJzcmNfYXNuIiwic3JjX2dlbyIsInNyY19yZWdpb24iLCJzcmNfY2l0eSIsInNyY19ob3N0bmFtZSIsInNyY19uYWljcyIsInNyY19zZWN0b3IiLCJkZXZpY2VfdmVuZG9yIiwiZGV2aWNlX3R5cGUiLCJkZXZpY2VfbW9kZWwiLCJpbmZlY3Rpb24iLCJmYW1pbHkiLCJ0YWciLCJxdWVyeV90eXBlIiwicXVlcnkiLCJjb3VudCIKIjIwMjItMDEtMDYgMDA6MDA6MDIiLCJ1ZHAiLCIyMDkuNjYuMC4wIiw0NjE4OSw0MDkzNCwiVVMiLCJWSVJHSU5JQSIsIkFTSEJVUk4iLCw1MTgyMTAsLCwsLCJvcmN1cyIsIm9yY3VzIiwicmF0IiwiQSIsInZlcmJsZS5yb2NrcyIsMQ==',
   'source.asn' : 40934,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'ASHBURN',
   'source.geolocation.region' : 'VIRGINIA',
   'source.ip' : '209.66.0.0',
   'source.port' : 46189,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-01-06T00:00:02+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sinkhole-dns',
   'extra.tag' : 'msexchange',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.count' : '1',
   'extra.infection' : 'calypso',
   'extra.query' : 'RAwFuNS.COM',
   'extra.query_type' : 'A',
   'extra.source.naics' : 518210,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'feed.name' : 'Sinkhole DNS',
   'malware.name' : 'calypso',
   'protocol.application' : 'dns',
   'protocol.transport' : 'udp',
   'raw' : 'InRpbWVzdGFtcCIsInByb3RvY29sIiwic3JjX2lwIiwic3JjX3BvcnQiLCJzcmNfYXNuIiwic3JjX2dlbyIsInNyY19yZWdpb24iLCJzcmNfY2l0eSIsInNyY19ob3N0bmFtZSIsInNyY19uYWljcyIsInNyY19zZWN0b3IiLCJkZXZpY2VfdmVuZG9yIiwiZGV2aWNlX3R5cGUiLCJkZXZpY2VfbW9kZWwiLCJpbmZlY3Rpb24iLCJmYW1pbHkiLCJ0YWciLCJxdWVyeV90eXBlIiwicXVlcnkiLCJjb3VudCIKIjIwMjItMDEtMDYgMDA6MDA6MDIiLCJ1ZHAiLCIyMTcuMTEwLjAuMCIsMzU5MCw4MjIwLCJERSIsIkhFU1NFTiIsIkZSQU5LRlVSVCBBTSBNQUlOIiwsNTE4MjEwLCJDb21tdW5pY2F0aW9ucywgU2VydmljZSBQcm92aWRlciwgYW5kIEhvc3RpbmcgU2VydmljZSIsLCwsImNhbHlwc28iLCJjYWx5cHNvIiwibXNleGNoYW5nZSIsIkEiLCJSQXdGdU5TLkNPTSIsMQ==',
   'source.asn' : 8220,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'FRANKFURT AM MAIN',
   'source.geolocation.region' : 'HESSEN',
   'source.ip' : '217.110.0.0',
   'source.port' : 3590,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-01-06T00:00:02+00:00'
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
