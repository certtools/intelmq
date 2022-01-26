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
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
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
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
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
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
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
