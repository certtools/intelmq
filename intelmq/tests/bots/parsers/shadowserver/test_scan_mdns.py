# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_mdns.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open mDNS',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_mdns-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open mDNS',
           "classification.identifier": "open-mdns",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.services": "_workstation.examplehostname.local.;",
           "extra.tag": "mdns",
           "extra.workstation_info": "[00:00:00:00:00:00]",
           "extra.workstation_ipv4": "198.51.100.176 198.51.100.176 198.51.100.176",
           "extra.workstation_name": "examplehostname.local.",
           "protocol.application": "mdns",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 24940,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "GUNZENHAUSEN",
           "source.geolocation.region": "BAYERN",
           "source.ip": "198.51.100.4",
           "source.port": 5353,
           "source.reverse_dns": "198-51-100-182.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T07:38:35+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open mDNS',
           "classification.identifier": "open-mdns",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.services": "_workstation.examplehostname.local.;",
           "extra.tag": "mdns",
           "extra.workstation_info": "[00:00:00:00:00:00]",
           "extra.workstation_ipv4": "198.51.100.176 198.51.100.176 198.51.100.176 198.51.100.176 198.51.100.176",
           "extra.workstation_ipv6": "2001:0db8:abcd:0012:0000:0000:0000:0000",
           "extra.workstation_name": "examplehostname.local.",
           "protocol.application": "mdns",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 24940,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "GUNZENHAUSEN",
           "source.geolocation.region": "BAYERN",
           "source.ip": "198.51.100.221",
           "source.port": 5353,
           "source.reverse_dns": "198-51-100-221.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T07:38:36+00:00"
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
