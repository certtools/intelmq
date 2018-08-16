# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'drone_brute_force.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Drone Brute Force",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'ssh',
           'classification.taxonomy': 'intrusion attempts',
           'classification.type': 'brute-force',
           'extra.client_version': 'SSH-2.0-libssh2_1.7.0',
           'destination.asn': 65536,
           'destination.geolocation.cc': 'CA',
           'destination.ip': '198.51.100.196',
           'destination.port': 22,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Information Technology',
           'extra.destination.sic': 737401,
           'extra.end_time': '2018-04-07T03:02:19.143501Z',
           'extra.password': 'password',
           'extra.public_source': 'SISSDEN',
           'extra.start_time': '2018-04-07T03:02:15.951205Z',
           'destination.account': 'alex',
           'protocol.application': 'ssh',
           'feed.name': 'ShadowServer Drone Brute Force',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 64496,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'WIEN',
           'source.geolocation.region': 'WIEN',
           'source.ip': '198.51.100.169',
           'source.port': 38880,
           'time.source': '2018-04-07T03:02:15+00:00'},
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Drone-Brute-Force'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
