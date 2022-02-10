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
                       'testdata/scan_synfulknock.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'SYNful Knock',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_synfulknock-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-synfulknock',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.ack_number' : 791102,
   'extra.raw_packet' : '3cfdfec601e4700f6a9a2000080045000034c3780000f706789442099555b869f7ee0050b20800000000000c123e8012200002aa0000020405b40101040201030305',
   'extra.tag' : 'synfulknock',
   'extra.tcp_flags' : '4608',
   'extra.window_size' : 8192,
   'feed.name' : 'SYNful Knock',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJzZXF1ZW5jZV9udW1iZXIiLCJhY2tfbnVtYmVyIiwid2luZG93X3NpemUiLCJ1cmdlbnRfcG9pbnRlciIsInRjcF9mbGFncyIsInJhd19wYWNrZXQiLCJzZWN0b3IiCiIyMDIyLTAxLTEwIDA5OjE4OjIzIiwiNjYuOS4wLjAiLCJ0Y3AiLDgwLCwic3luZnVsa25vY2siLDE4ODg1LCJVUyIsIk5FVyBKRVJTRVkiLCJKRVJTRVkgQ0lUWSIsLCwwLDc5MTEwMiw4MTkyLDAsNDYwOCwiM2NmZGZlYzYwMWU0NzAwZjZhOWEyMDAwMDgwMDQ1MDAwMDM0YzM3ODAwMDBmNzA2Nzg5NDQyMDk5NTU1Yjg2OWY3ZWUwMDUwYjIwODAwMDAwMDAwMDAwYzEyM2U4MDEyMjAwMDAyYWEwMDAwMDIwNDA1YjQwMTAxMDQwMjAxMDMwMzA1Iiw=',
   'source.asn' : 18885,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'JERSEY CITY',
   'source.geolocation.region' : 'NEW JERSEY',
   'source.ip' : '66.9.0.0',
   'source.port' : 80,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T09:18:23+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-synfulknock',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.ack_number' : 791102,
   'extra.raw_packet' : '90e2baaf0b84700f6a9a200008004500003434100000f2064382d58337d2b8698b720050916200000000000c123e8012200059d50000020405b40101040201030305',
   'extra.tag' : 'synfulknock',
   'extra.tcp_flags' : '4608',
   'extra.window_size' : 8192,
   'feed.name' : 'SYNful Knock',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJzZXF1ZW5jZV9udW1iZXIiLCJhY2tfbnVtYmVyIiwid2luZG93X3NpemUiLCJ1cmdlbnRfcG9pbnRlciIsInRjcF9mbGFncyIsInJhd19wYWNrZXQiLCJzZWN0b3IiCiIyMDIyLTAxLTEwIDA5OjE5OjE3IiwiMjEzLjEzMS4wLjAiLCJ0Y3AiLDgwLCJob3N0LTIxMy0xMzEtNTUtMjEwLWN1c3RvbWVyLndhbmV4Lm5ldCIsInN5bmZ1bGtub2NrIiwzNTgwNSwiR0UiLCJUQklMSVNJIiwiVEJJTElTSSIsLCwwLDc5MTEwMiw4MTkyLDAsNDYwOCwiOTBlMmJhYWYwYjg0NzAwZjZhOWEyMDAwMDgwMDQ1MDAwMDM0MzQxMDAwMDBmMjA2NDM4MmQ1ODMzN2QyYjg2OThiNzIwMDUwOTE2MjAwMDAwMDAwMDAwYzEyM2U4MDEyMjAwMDU5ZDUwMDAwMDIwNDA1YjQwMTAxMDQwMjAxMDMwMzA1Iiw=',
   'source.asn' : 35805,
   'source.geolocation.cc' : 'GE',
   'source.geolocation.city' : 'TBILISI',
   'source.geolocation.region' : 'TBILISI',
   'source.ip' : '213.131.0.0',
   'source.port' : 80,
   'source.reverse_dns' : 'host-213-131-55-210-customer.wanex.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T09:19:17+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-synfulknock',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.ack_number' : 791102,
   'extra.raw_packet' : '90e2bab9cfd4700f6a9a20000800450000340f1d0000ea068bdad5b2e6914a522f360050eb5200000000000c123e801220001b4a0000020405b40101040201030305',
   'extra.tag' : 'synfulknock',
   'extra.tcp_flags' : '4608',
   'extra.window_size' : 8192,
   'feed.name' : 'SYNful Knock',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJzZXF1ZW5jZV9udW1iZXIiLCJhY2tfbnVtYmVyIiwid2luZG93X3NpemUiLCJ1cmdlbnRfcG9pbnRlciIsInRjcF9mbGFncyIsInJhd19wYWNrZXQiLCJzZWN0b3IiCiIyMDIyLTAxLTEwIDA5OjI3OjM5IiwiMjEzLjE3OC4wLjAiLCJ0Y3AiLDgwLCwic3luZnVsa25vY2siLDI5MjU2LCJTWSIsIkRJTUFTSFEiLCJEQU1BU0NVUyIsLCwwLDc5MTEwMiw4MTkyLDAsNDYwOCwiOTBlMmJhYjljZmQ0NzAwZjZhOWEyMDAwMDgwMDQ1MDAwMDM0MGYxZDAwMDBlYTA2OGJkYWQ1YjJlNjkxNGE1MjJmMzYwMDUwZWI1MjAwMDAwMDAwMDAwYzEyM2U4MDEyMjAwMDFiNGEwMDAwMDIwNDA1YjQwMTAxMDQwMjAxMDMwMzA1Ig==',
   'source.asn' : 29256,
   'source.geolocation.cc' : 'SY',
   'source.geolocation.city' : 'DAMASCUS',
   'source.geolocation.region' : 'DIMASHQ',
   'source.ip' : '213.178.0.0',
   'source.port' : 80,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T09:27:39+00:00'
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
