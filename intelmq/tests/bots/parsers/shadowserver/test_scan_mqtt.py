# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_mqtt.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open-MQTT',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2020-03-15T00:00:00+00:00",
                  "extra.file_name": "2020-03-14-scan_mqtt-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open-MQTT',
           "classification.identifier": "open-mqtt",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.anonymous_access": True,
           "extra.code": "Connection Accepted",
           "extra.hex_code": "00",
           "extra.naics": 518210,
           "extra.raw_response": "20020000",
           "extra.tag": "mqtt",
           "protocol.application": "mqtt",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 12345,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "CITY",
           "source.geolocation.region": "REGION",
           "source.ip": "123.45.67.89",
           "source.port": 1883,
           'source.reverse_dns': 'some.host.com',
           "time.observation": "2020-03-15T00:00:00+00:00",
           "time.source": "2020-03-14T05:45:48+00:00"
           },
{'__type': 'Event',
           'feed.name': 'Open-MQTT',
           "classification.identifier": "open-mqtt",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.anonymous_access": False,
           "extra.code": "Connection Refused, Server unavailable",
           "extra.hex_code": "03",
           "extra.naics": 454110,
           "extra.raw_response": "20020003",
           "extra.tag": "mqtt",
           "protocol.application": "mqtt",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 12345,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "CITY",
           "source.geolocation.region": "REGION",
           "source.ip": "123.45.67.90",
           "source.port": 1883,
           'source.reverse_dns': 'another.host.com',
           "time.observation": "2020-03-15T00:00:00+00:00",
           "time.source": "2020-03-14T05:45:51+00:00"
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
