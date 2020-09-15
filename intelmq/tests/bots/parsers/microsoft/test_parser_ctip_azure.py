# -*- coding: utf-8 -*-
import json
import os
import unittest

from intelmq.bots.parsers.microsoft.parser_ctip import MicrosoftCTIPParserBot
from intelmq.lib import test
from intelmq.lib.utils import base64_encode


with open(os.path.join(os.path.dirname(__file__), 'ctip_azure.txt')) as handle:
    EXAMPLE_DATA = handle.read()
EXAMPLE_LINES = EXAMPLE_DATA.splitlines()
EXAMPLE_PARSED = [json.loads(EXAMPLE_LINES[0]), json.loads(EXAMPLE_LINES[1])]


EXAMPLE_REPORT = {
    "__type": "Report",
    "feed.accuracy": 100.0,
    "time.observation": "2016-06-15T09:25:26+00:00",
    "raw": base64_encode(EXAMPLE_DATA)
}

EXAMPLE_TEMPLATE = {
    "feed.name": "CTIP-Infected",
    "event_description.text": "SinkHoleMessage",
    "tlp": "AMBER",
    }


EXAMPLE_EVENTS = [{
    "__type": "Event",
    'feed.accuracy': 20.0,
    'classification.type': 'infected-system',
    'destination.ip': '198.18.18.18',
    'destination.port': 80,
    'malware.name': 'b67-ss-tinba',
    'source.asn': 64496,
    'source.ip': '224.0.5.8',
"extra.total_encounters": 3,
    "source.port": 65116,
    "time.source": "2020-05-24T22:45:28.487000+00:00",
    "source.as_name": "Example AS 1",
    "source.geolocation.cc": "AT",
    "source.geolocation.latitude": 48.2,
    "source.geolocation.longitude": 16.3667,
    "extra.custom_field1": "tinba",
    "raw": base64_encode(EXAMPLE_LINES[0]),
    "extra.payload.timestamp": '2020-05-24T22:45:28.487420+00:00',
    "extra.payload.ip": "127.0.0.1",
    "extra.payload.port" :65116,
    "extra.payload.server.ip": "198.18.185.162",
    "extra.payload.server.port": 80,
    "extra.payload.domain": "example.com",
    "extra.payload.family":"tinba",
    "extra.payload.response":"Response",
    "extra.payload.handler":"tinba",
    "protocol.application":"http",
    'extra.malware': 'Avalanche',
    }, {
    "__type": "Event",
    'feed.accuracy': 100.0,
    'classification.type': 'infected-system',
    'destination.ip': '198.18.18.18',
    'destination.port': 80,
    'malware.name': 'b67-ss-matsnu',
"extra.total_encounters": 5,
    'source.asn': 64497,
    'source.ip': '224.0.5.8',
    "source.port": 49296,
    "time.source": "2020-05-24T22:47:43.050999+00:00",
    "source.as_name": "Example AS 2",
    "source.geolocation.cc": "AT",
    "source.geolocation.latitude": 48.1951,
    "source.geolocation.longitude": 16.3483,
"extra.source.geolocation.area_code": 9,
"extra.source.geolocation.postal_code": '1060',
"source.geolocation.region": "Vienna",
"source.geolocation.city": "Vienna",
    "extra.custom_field1": "matsnu5",
    "raw": base64_encode(EXAMPLE_LINES[1]),
    "extra.payload.text": 'this is just some text',
    'extra.malware': 'Avalanche',
    },
    ]

for index, data in enumerate(EXAMPLE_EVENTS):
    EXAMPLE_EVENTS[index].update(EXAMPLE_TEMPLATE)


class TestMicrosoftCTIPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for the MicrosoftCTIPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MicrosoftCTIPParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test with azure format. """
        self.run_bot()
        for i in range(2):
            self.assertMessageEqual(i, EXAMPLE_EVENTS[i])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
