# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_telnet.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible Telnet',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_telnet-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible Telnet',
           "classification.identifier": "open-telnet",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.banner": "|MikroTik v6.5|Login:",
           "extra.tag": "telnet-alt",
           "protocol.application": "telnet",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 20255,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.145",
           "source.port": 5678,
           "source.reverse_dns": "example.local",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T12:27:34+00:00"
          },
          {'__type': 'Event',
           'feed.name': 'Accessible Telnet',
           "classification.identifier": "open-telnet",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.banner": "|MikroTik v6.45.3 (stable)|Login:",
           "extra.tag": "telnet-alt",
           "protocol.application": "telnet",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 20255,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.145",
           "source.port": 5678,
           "source.reverse_dns": "example.local",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T12:27:40+00:00"
          }]


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
