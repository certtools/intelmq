# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_coap.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible-CoAP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2020-06-29T00:00:00+00:00",
                  "extra.file_name": "2020-06-28-scan_coap-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible-CoAP',
           "classification.identifier": "accessible-coap",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           'extra.naics': 518210,
           "extra.response": "</api>,</api/v1>,</.well-known/core>",
           "extra.tag": "coap",
           "protocol.application": "coap",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 12345,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "CITY",
           "source.geolocation.region": "REGION",
           "source.ip": "123.45.67.89",
           "source.port": 5683,
           'source.reverse_dns': 'some.host.com',
           "time.observation": "2020-06-29T00:00:00+00:00",
           "time.source": "2020-06-28T03:45:24+00:00"
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
