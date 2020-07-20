# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ard.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible ARD',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2020-07-20T00:00:00+00:00",
                  "extra.file_name": "2020-01-01-scan_ard-test-test.csv",

                  }
EVENTS = [{
    '__type': 'Event',
    'feed.name': 'Accessible ARD',
    "classification.identifier": "accessible-ard",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.machine_name": "LPG2.ucmerced.edu",
    "extra.naics": 611310,
    "extra.sic": 822101,
    "extra.response_size": 1006,
    "extra.tag": "ard",
    "protocol.transport": "udp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
    "source.asn": 22323,
    "source.geolocation.cc": "US",
    "source.geolocation.city": "MERCED",
    "source.geolocation.region": "CALIFORNIA",
    "source.ip": "169.236.55.189",
    "source.port": 3283,
    "source.reverse_dns": "lpg2.ucmerced.edu",
    "time.observation": "2020-07-20T00:00:00+00:00",
    "time.source": "2019-10-02T09:18:05+00:00"
},
{
    '__type': 'Event',
    'feed.name': 'Accessible ARD',
    "classification.identifier": "accessible-ard",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.machine_name": "Surveillance System - Greenlea",
    "extra.naics": 517312,
    "extra.sic": 737415,
    "extra.response_size": 1006,
    "extra.tag": "ard",
    "protocol.transport": "udp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
    "source.asn": 701,
    "source.geolocation.cc": "US",
    "source.geolocation.city": "SYRACUSE",
    "source.geolocation.region": "NEW YORK",
    "source.ip": "74.111.20.19",
    "source.port": 3283,
    "source.reverse_dns": "static-74-111-20-19.syrcny.fios.verizon.net",
    "time.observation": "2020-07-20T00:00:00+00:00",
    "time.source": "2019-10-02T09:18:06+00:00"
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
