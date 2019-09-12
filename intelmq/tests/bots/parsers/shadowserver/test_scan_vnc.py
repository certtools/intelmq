# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
          'testdata/scan_vnc.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible VNC',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_vnc-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible VNC',
           "classification.identifier": "open-vnc",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.banner": "RFB 003.889",
           "extra.product": "Apple remote desktop vnc",
           "protocol.application": "vnc",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.53",
           "source.port": 5678,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T14:51:44+00:00"
          },
          {'__type': 'Event',
           'feed.name': 'Accessible VNC',
           "classification.identifier": "open-vnc",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.banner": "RFB 005.000",
           "extra.naics": 517311,
           "extra.product": "RealVNC Enterprise v5.3 or later",
           "protocol.application": "vnc",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.112",
           "source.port": 5678,
           "source.reverse_dns": "localhost.localdomain",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T14:51:44+00:00"}]


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
