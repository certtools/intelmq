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
                       'testdata/special.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Special',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-special-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier': 'special',
   'classification.taxonomy': 'vulnerable',
   'classification.type': 'vulnerable-system',
   'extra.method' : 'dns',
   'extra.public_source' : 'alphastrike.io',
   'extra.status' : 'vulnerable',
   'feed.name' : 'Special',
   'malware.name' : 'cve-2021-44228',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 48715,
   'source.geolocation.cc' : 'IR',
   'source.geolocation.city' : 'TEHRAN',
   'source.geolocation.region' : 'TEHRAN',
   'source.ip' : '185.36.0.0',
   'source.port' : 80,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2021-12-16T19:23:43+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'special',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.method' : 'dns',
   'extra.public_source' : 'alphastrike.io',
   'extra.source.naics' : 517311,
   'extra.status' : 'vulnerable',
   'feed.name' : 'Special',
   'malware.name' : 'cve-2021-44228',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 134756,
   'source.geolocation.cc' : 'CN',
   'source.geolocation.city' : 'NANJING',
   'source.geolocation.region' : 'JIANGSU SHENG',
   'source.ip' : '58.213.0.0',
   'source.port' : 80,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2021-12-16T19:23:44+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'special',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.method' : 'dns',
   'extra.public_source' : 'alphastrike.io',
   'extra.source.naics' : 517312,
   'extra.status' : 'vulnerable',
   'feed.name' : 'Special',
   'malware.name' : 'cve-2021-44228',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 56046,
   'source.geolocation.cc' : 'CN',
   'source.geolocation.city' : 'FUZHOU',
   'source.geolocation.region' : 'FUJIAN SHENG',
   'source.ip' : '36.156.0.0',
   'source.port' : 80,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2021-12-16T19:23:44+00:00'
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
