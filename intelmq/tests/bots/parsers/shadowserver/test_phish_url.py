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
                       'testdata/phish_url.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Phish URL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-phish_url-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'phish-url',
   'classification.taxonomy' : 'fraud',
   'classification.type' : 'phishing',
   'source.fqdn' : 'priceless-pare.example.net',
   'extra.source' : 'openphish.com',
   'extra.source.naics' : 518210,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'source.url' : 'https://priceless-pare.example.net/Postal-/acec6/',
   'feed.name' : 'Phish URL',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'BUFFALO',
   'source.geolocation.region' : 'NEW YORK',
   'source.ip' : '172.245.0.0',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-02-01T08:00:07+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'phish-url',
   'classification.taxonomy' : 'fraud',
   'classification.type' : 'phishing',
   'source.fqdn' : 'mailyahooattt.example.net',
   'extra.source' : 'openphish.com',
   'extra.source.sector' : 'Professional, Scientific, and Technical Services',
   'source.url' : 'https://mailyahooattt.example.net/',
   'feed.name' : 'Phish URL',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'SAN FRANCISCO',
   'source.geolocation.region' : 'CALIFORNIA',
   'source.ip' : '199.34.0.0',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-02-01T08:00:07+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'phish-url',
   'classification.taxonomy' : 'fraud',
   'classification.type' : 'phishing',
   'source.fqdn' : 'www.example.net',
   'extra.source' : 'openphish.com',
   'extra.source.naics' : 519130,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'source.url' : 'https://www.example.net/viewer/vbid-730ec2b1-omsttuer',
   'feed.name' : 'Phish URL',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'DRAPER',
   'source.geolocation.region' : 'UTAH',
   'source.ip' : '216.58.0.0',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-02-01T08:00:07+00:00'
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
