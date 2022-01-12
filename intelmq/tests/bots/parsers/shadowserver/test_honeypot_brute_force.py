# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/event4_honeypot_brute_force.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Drone Brute Force',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_honeypot_brute_force.csv"
                  }
EVENTS = [{'__type': 'Event',
           'classification.taxonomy': 'intrusion-attempts',
           'classification.type': 'brute-force',
           'extra.client_version': "b'SSH-2.0-Go'",
           'destination.asn': 26832,
           'destination.geolocation.cc': 'CA',
           'destination.geolocation.city': 'MONTREAL',
           'destination.geolocation.region': 'QUEBEC',
           'destination.ip': '162.250.1.2',
           'destination.port': 22,
           'extra.application': 'ssh',
           'extra.end_time': '2021-03-27T00:00:01.710968+00:00',
           'extra.public_source': 'CAPRICA-EU',
           'extra.start_time': '2021-03-27T00:00:00.521730Z',
           'malware.name': 'ssh-brute-force',
           'feed.name': 'Drone Brute Force',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 209588,
           'source.geolocation.cc': 'NL',
           'source.geolocation.city': 'AMSTERDAM',
           'source.geolocation.region': 'NOORD-HOLLAND',
           'source.ip': '141.98.1.2',
           'source.port': 30123,
           'time.source': '2021-03-27T00:00:00+00:00'},
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
