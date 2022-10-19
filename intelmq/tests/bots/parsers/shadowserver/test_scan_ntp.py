# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_ntp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'NTP Version',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ntp-test-geo.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'ntp-version',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 27.0,
    'extra.clock': '0xe6ac3809.363028e7',
    'extra.frequency': 2.018,
    'extra.jitter': 0.977,
    'extra.leap': 0.0,
    'extra.noise': '0.984',
    'extra.offset': 0.557,
    'extra.peer': 18986,
    'extra.poll': 10,
    'extra.precision': -10,
    'extra.refid': '81.15.252.130',
    'extra.reftime': '0xe6ac35ba.2d2e8f2b',
    'extra.response_size': 324,
    'extra.rootdelay': 17.685,
    'extra.rootdispersion': 61.254,
    'extra.stability': '0.027',
    'extra.state': '4',
    'extra.stratum': 4,
    'extra.system': 'UNIX',
    'extra.tag': 'ntpversion',
    'extra.version': '4',
    'feed.name': 'NTP Version',
    'protocol.application': 'ntp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 123,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'ntp-version',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 27.33,
    'extra.clk_wander': 0.007,
    'extra.clock': '0xE6AC3806.7DF3B7A0',
    'extra.frequency': -20.407,
    'extra.jitter': 8.776,
    'extra.leap': 0.0,
    'extra.mintc': '3',
    'extra.offset': -14.502,
    'extra.peer': 19244,
    'extra.precision': -10,
    'extra.refid': '10.48.21.21',
    'extra.reftime': '0xE6AC3431.B3B64790',
    'extra.response_size': 328,
    'extra.rootdelay': 32.25,
    'extra.rootdispersion': 105.778,
    'extra.sector': 'Transportation and Warehousing',
    'extra.stratum': 8,
    'extra.system': 'UNIX',
    'extra.tag': 'ntpversion',
    'extra.tc': 10,
    'extra.version': '4',
    'feed.name': 'NTP Version',
    'protocol.application': 'ntp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 123,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'ntp-version',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 27.0,
    'extra.clk_wander': 0.001,
    'extra.clock': '0xE6AC380A.5A1CAD00',
    'extra.frequency': -24.01,
    'extra.jitter': 2.343,
    'extra.leap': 0.0,
    'extra.mintc': '3',
    'extra.offset': 0.49,
    'extra.peer': 51892,
    'extra.precision': -10,
    'extra.refid': '172.28.0.1',
    'extra.reftime': '0xE6AC3020.0C49BA80',
    'extra.response_size': 324,
    'extra.rootdelay': 7.749,
    'extra.rootdispersion': 81.612,
    'extra.stratum': 4,
    'extra.system': 'UNIX',
    'extra.tag': 'ntpversion',
    'extra.tc': 10,
    'extra.version': '4',
    'feed.name': 'NTP Version',
    'protocol.application': 'ntp',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 123,
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
