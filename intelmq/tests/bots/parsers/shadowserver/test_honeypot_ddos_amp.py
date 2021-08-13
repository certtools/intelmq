# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/event4_honeypot_ddos_amp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Amplification DDoS Victim',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_honeypot_ddos_amp.csv"
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Amplification DDoS Victim',
           'classification.identifier': 'amplification-ddos-victim',
           'classification.taxonomy': 'availability',
           'classification.type': 'ddos',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2019-01-01T00:00:00+00:00',
           'time.source': '2021-03-28T00:00:02+00:00',
           'source.ip': '107.141.1.2',
           'destination.port': 389,
           'source.reverse_dns': '192-0-2-10.example.net',
           'source.asn': 7018,
           'source.geolocation.cc': 'US',
           'source.geolocation.region': 'VISALIA',
           'source.geolocation.city': 'VISALIA',
           'source.geolocation.region': 'CALIFORNIA',
           'extra.end_time': '2021-03-28T00:20:22+00:00',
           'extra.public_source': 'CISPA',
           'extra.source.naics': 517311,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'malware.name': 'ddos-amplification',
           'source.reverse_dns': '107-141-x-x.lightspeed.frsnca.sbcglobal.net',
           },
           {'__type': 'Event',
           'feed.name': 'Amplification DDoS Victim',
           'classification.identifier': 'amplification-ddos-victim',
           'classification.taxonomy': 'availability',
           'classification.type': 'ddos',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': '2019-01-01T00:00:00+00:00',
           'time.source': '2021-03-28T00:00:02+00:00',
           'source.ip': '74.59.3.4',
           'destination.port': 389,
           'source.reverse_dns': 'modemcablex-x-59-74.mc.videotron.ca',
           'source.asn': 5769,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'CHICOUTIMI',
           'source.geolocation.region': 'QUEBEC',
           'extra.end_time': '2021-03-28T00:13:50+00:00',
           'extra.public_source': 'CISPA',
           'extra.source.naics': 517311,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'malware.name': 'ddos-amplification',
           },
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
