import os
import json

import unittest

from intelmq.lib import test, utils
from intelmq.bots.parsers.cznic.parser_proki import CZNICProkiParserBot

with open(os.path.join(os.path.dirname(__file__), "example_proki.json")) as handle:
    INPUT = handle.read()
INPUT_EVENTS = json.loads(INPUT).get("data")

EXAMPLE_REPORT = {
    "feed.url": "",
    "__type": "Report",
    "raw": utils.base64_encode(INPUT),
}

EXAMPLE_EVENT = {
    "malware.name": "conficker",
    "destination.geolocation.longitude": 0.000,
    "destination.asn": 64500,
    "destination.port": 80,
    "source.asn": 64501,
    "destination.geolocation.cc": "ZZ",
    "extra.original_feed_name": "spamhaus-cert",
    "destination.abuse_contact": "contact@example.com",
    "destination.geolocation.latitude": 0.000,
    "classification.type": "infected-system",
    "source.geolocation.city": "city",
    "destination.network": "192.0.2.0/24",
    "source.ip": "192.0.3.1",
    "source.geolocation.latitude": 0.000,
    "protocol.transport": "tcp",
    "extra.original_time_observation": "2020-08-12T14:42:42+00:00",
    "extra.source.local_port": 18392,
    "source.network": "192.0.3.0/24",
    "destination.ip": "192.0.2.1",
    "time.source": "2020-08-12T13:32:31+00:00",
    "source.geolocation.longitude": 0.000,
    "classification.taxonomy": "malicious code",
    "source.geolocation.cc": "ZZ",
    "feed.accuracy": 100.00,
    "source.abuse_contact": "contact@example.com",
    "raw": utils.base64_encode("[" + json.dumps(INPUT_EVENTS[0], separators=(", ", ": "),) + "]"),
    "__type": "Event",
}


class TestCZNICProkiParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CZNICProkiParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CZNICProkiParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == "__main__":
    unittest.main()
