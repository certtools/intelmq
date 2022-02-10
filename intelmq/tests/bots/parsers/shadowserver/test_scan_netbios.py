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
                       'testdata/scan_netbios.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Netbios',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_netbios-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-netbios',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.mac_address' : '00-00-00-00-00-00',
   'extra.machine_name' : 'EXAMPLEMACHINE',
   'extra.source.naics' : 541690,
   'extra.source.sic' : 874899,
   'extra.tag' : 'netbios',
   'extra.username' : 'DEV',
   'extra.workgroup' : 'ARBEITSGRUPPE',
   'feed.name' : 'Netbios',
   'protocol.application' : 'netbios-nameservice',
   'protocol.transport' : 'udp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJtYWNfYWRkcmVzcyIsImFzbiIsImdlbyIsInJlZ2lvbiIsImNpdHkiLCJ3b3JrZ3JvdXAiLCJtYWNoaW5lX25hbWUiLCJ1c2VybmFtZSIsIm5haWNzIiwic2ljIiwic2VjdG9yIgoiMjAxNi0wNy0yNCAwMDoxMDo1MCIsIjE5OC41MS4xMDAuNCIsInVkcCIsMTM3LCIxOTgtNTEtMTAwLTQuZXhhbXBsZS5uZXQiLCJuZXRiaW9zIiwiMDAtMDAtMDAtMDAtMDAtMDAiLDMzMjAsIkRFIiwiQkFERU4tV1VSVFRFTUJFUkciLCJTSU5ERUxGSU5HRU4iLCJBUkJFSVRTR1JVUFBFIiwiRVhBTVBMRU1BQ0hJTkUiLCJERVYiLDU0MTY5MCw4NzQ4OTks',
   'source.asn' : 3320,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'SINDELFINGEN',
   'source.geolocation.region' : 'BADEN-WURTTEMBERG',
   'source.ip' : '198.51.100.4',
   'source.port' : 137,
   'source.reverse_dns' : '198-51-100-4.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2016-07-24T00:10:50+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-netbios',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.mac_address' : '00-1B-C6-41-35-F5',
   'extra.machine_name' : 'EXAMPLEMACHINE',
   'extra.tag' : 'netbios',
   'extra.workgroup' : 'STRATOSERVER',
   'feed.name' : 'Netbios',
   'protocol.application' : 'netbios-nameservice',
   'protocol.transport' : 'udp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJtYWNfYWRkcmVzcyIsImFzbiIsImdlbyIsInJlZ2lvbiIsImNpdHkiLCJ3b3JrZ3JvdXAiLCJtYWNoaW5lX25hbWUiLCJ1c2VybmFtZSIsIm5haWNzIiwic2ljIiwic2VjdG9yIgoiMjAxNi0wNy0yNCAwMDoxMDo1MCIsIjE5OC41MS4xMDAuMTgyIiwidWRwIiwxMzcsIjE5OC01MS0xMDAtMTgyLmV4YW1wbGUubmV0IiwibmV0YmlvcyIsIjAwLTFCLUM2LTQxLTM1LUY1Iiw2NzI0LCJERSIsIkJFUkxJTiIsIkJFUkxJTiIsIlNUUkFUT1NFUlZFUiIsIkVYQU1QTEVNQUNISU5FIiwsMCwwLA==',
   'source.asn' : 6724,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'BERLIN',
   'source.geolocation.region' : 'BERLIN',
   'source.ip' : '198.51.100.182',
   'source.port' : 137,
   'source.reverse_dns' : '198-51-100-182.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2016-07-24T00:10:50+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-netbios',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.mac_address' : '00-00-00-00-00-00',
   'extra.machine_name' : 'EXAMPLEMACHINE',
   'extra.tag' : 'netbios',
   'extra.username' : 'DEV',
   'extra.workgroup' : 'WORKGROUP',
   'feed.name' : 'Netbios',
   'protocol.application' : 'netbios-nameservice',
   'protocol.transport' : 'udp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJtYWNfYWRkcmVzcyIsImFzbiIsImdlbyIsInJlZ2lvbiIsImNpdHkiLCJ3b3JrZ3JvdXAiLCJtYWNoaW5lX25hbWUiLCJ1c2VybmFtZSIsIm5haWNzIiwic2ljIiwic2VjdG9yIgoiMjAxNi0wNy0yNCAwMDoxMDo1MCIsIjE5OC41MS4xMDAuMTc2IiwidWRwIiwxMzcsIjE5OC01MS0xMDAtMjIxLmV4YW1wbGUubmV0IiwibmV0YmlvcyIsIjAwLTAwLTAwLTAwLTAwLTAwIiwyNDk0MCwiREUiLCJCQVlFUk4iLCJHVU5aRU5IQVVTRU4iLCJXT1JLR1JPVVAiLCJFWEFNUExFTUFDSElORSIsIkRFViIsMCwwLA==',
   'source.asn' : 24940,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'GUNZENHAUSEN',
   'source.geolocation.region' : 'BAYERN',
   'source.ip' : '198.51.100.176',
   'source.port' : 137,
   'source.reverse_dns' : '198-51-100-221.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2016-07-24T00:10:50+00:00'
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
