# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_isakmp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Vulnerable ISAKMP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_isakmp-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Vulnerable ISAKMP',
           "classification.identifier": "open-ike",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.domain_of_interpretation": 0,
           "extra.exchange_type": 5,
           "extra.flags": 0,
           "extra.initiator_spi": "3e35c70729dfedef",
           "extra.message_id": "00000000",
           "extra.naics": 517311,
           "extra.next_payload": 11,
           "extra.next_payload2": 0,
           "extra.notify_message_type": 14,
           "extra.responder_spi": "253acab7cbfda607",
           "extra.spi_size": 0,
           "extra.tag": "isakmp-vulnerable",
           "protocol.application": "ipsec",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.42",
           "source.port": 500,
           "source.reverse_dns": "example.local",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T00:17:25+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Vulnerable ISAKMP',
           "classification.identifier": "open-ike",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.domain_of_interpretation": 0,
           "extra.exchange_type": 5,
           "extra.flags": 0,
           "extra.initiator_spi": "3e35c70729dfedef",
           "extra.message_id": "00000000",
           "extra.next_payload": 11,
           "extra.next_payload2": 0,
           "extra.notify_message_type": 14,
           "extra.responder_spi": "b274460e7adc1bf0",
           "extra.spi_size": 0,
           "extra.tag": "isakmp-vulnerable",
           "protocol.application": "ipsec",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 20255,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.67",
           "source.port": 500,
           "source.reverse_dns": "example.local",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T00:17:28+00:00"
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
