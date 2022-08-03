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
   'classification.identifier' : 'special',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.status' : 'likely compromised',
   'feed.name' : 'Special',
   'malware.name' : 'cyclops-blink',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'special',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.status' : 'likely compromised',
   'feed.name' : 'Special',
   'malware.name' : 'cyclops-blink',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'special',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.source.sector' : 'Professional, Scientific, and Technical Services',
   'extra.status' : 'likely compromised',
   'feed.name' : 'Special',
   'malware.name' : 'cyclops-blink',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.reverse_dns' : 'node03.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:02+00:00'
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
