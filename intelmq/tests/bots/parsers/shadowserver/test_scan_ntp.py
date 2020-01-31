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
EVENTS = [{'__type': 'Event',
           'feed.name': 'NTP Version',
           "classification.identifier": "ntp-version",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.clk_wander": 0.0,
           "extra.clock": "0xE1198EEB.21E18AD4",
           "extra.frequency": 0.0,
           "extra.jitter": 0.0,
           "extra.leap": 0,
           "extra.mintc": "3",
           "extra.naics": 517311,
           "extra.offset": 0.0,
           "extra.precision": -22,
           "extra.refid": "198.123.245.4",
           "extra.reftime": "0xE1198C78.D013546A",
           "extra.rootdelay": 0.0,
           "extra.rootdispersion": 0.0,
           "extra.stratum": 2,
           "extra.system": "UNIX",
           "extra.tc": 7,
           "extra.version": "4",
           "protocol.application": "ntp",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.134",
           "source.port": 123,
           "source.reverse_dns": "example.local",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T01:16:27+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'NTP Version',
           "classification.identifier": "ntp-version",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.clock": "0xE1198EEB.1675E416",
           "extra.error": "0.06",
           "extra.frequency": 153.78,
           "extra.leap": 0,
           "extra.naics": 517311,
           "extra.peer": 62164,
           "extra.poll": 6,
           "extra.refid": "198.123.245.123",
           "extra.reftime": "0xE1198EE2.84FFA639",
           "extra.rootdelay": 2.24,
           "extra.rootdispersion": 1.46,
           "extra.stratum": 2,
           "extra.system": "cisco",
           "protocol.application": "ntp",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.51",
           "source.port": 123,
           "source.reverse_dns": "example.local",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T01:16:27+00:00"
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
