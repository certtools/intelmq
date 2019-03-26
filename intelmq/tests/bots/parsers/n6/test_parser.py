# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.n6.parser_n6stomp import N6StompParserBot

EXAMPLE_REPORT = {"raw": "eyJjYXRlZ29yeSI6ICJib3RzIiwgIm9yaWdpbiI6ICJzaW5raG9sZSIsICJjb25maWRlbmNlIjogImhpZ2giLCAibmFtZSI6ICJzYWxpdHkiLCAicHJvdG8iOiAidGNwIiwgImFkZHJlc3MiOiBbeyJjYyI6ICJVUyIsICJpcCI6ICI2OC42OC45Ni4yMzUiLCAiYXNuIjogMTg3Nzl9XSwgInNvdXJjZSI6ICJjZXJ0LXBsLnNpbmtob2xlIiwgImFkaXAiOiAieC54LjExMS45OSIsICJ0aW1lIjogIjIwMTUtMTEtMTdUMTI6MTc6MjcuMDQzNDUyWiIsICJkcG9ydCI6IDgwLCAic3BvcnQiOiAyMjMwOCwgInR5cGUiOiAiZXZlbnQiLCAiaWQiOiAiZDc3YWU4Y2Y2ODFkY2RiYjZlMjAwMTQ1ODE0MDFlZDUifQ==",  # noqa
                  "__type": "Report",
                  "time.observation": "2015-11-17T12:17:27.043452Z",
                  }
EXAMPLE_EVENT = {"source.ip": "68.68.96.235",
                 "time.source": "2015-11-17T12:17:27.043452+00:00",
                 "classification.taxonomy": "malicious code",
                 "extra.adip": "x.x.111.99",
                 "extra.feed_id": "d77ae8cf681dcdbb6e20014581401ed5",
                 "source.port": 22308,
                 "time.observation": "2015-11-17T12:17:27.043452Z",
                 "source.geolocation.cc": "US",
                 "raw": "eyJjYXRlZ29yeSI6ICJib3RzIiwgIm9yaWdpbiI6ICJzaW5raG9sZSIsICJjb25maWRlbmNlIjogImhpZ2giLCAibmFtZSI6ICJzYWxpdHkiLCAicHJvdG8iOiAidGNwIiwgImFkZHJlc3MiOiBbeyJjYyI6ICJVUyIsICJpcCI6ICI2OC42OC45Ni4yMzUiLCAiYXNuIjogMTg3Nzl9XSwgInNvdXJjZSI6ICJjZXJ0LXBsLnNpbmtob2xlIiwgImFkaXAiOiAieC54LjExMS45OSIsICJ0aW1lIjogIjIwMTUtMTEtMTdUMTI6MTc6MjcuMDQzNDUyWiIsICJkcG9ydCI6IDgwLCAic3BvcnQiOiAyMjMwOCwgInR5cGUiOiAiZXZlbnQiLCAiaWQiOiAiZDc3YWU4Y2Y2ODFkY2RiYjZlMjAwMTQ1ODE0MDFlZDUifQ==",  # noqa
                 "classification.identifier": "sality",
                 "malware.name": "sality",
                 "classification.type": "infected system",
                 "destination.port": 80,
                 "__type": "Event",
                 "protocol.transport": "tcp",
                 "source.asn": 18779,
                 'extra.confidence': 'high',
                 'extra.feed_source': 'cert-pl.sinkhole',
                 }
BLACKLIST_REPORT = {"__type": "Report",
                    "raw": utils.base64_encode("""
    {"category": "other", "confidence": "low", "expires": "2019-02-03T20:12:03Z", "fqdn": "example.com", "source": "example", "time": "2019-01-12T23:12:02Z", "type": "bl-update", "id": "some hex string", "address": [{"cc": "AT", "ip": "10.0.0.1", "asn": 65536}]}
                                     """),
                    "time.observation": "2015-11-17T12:17:27.043452Z",
                    }
BLACKLIST_EVENT = {"__type": "Event",
                   "classification.taxonomy": "other",
                   "classification.type": "blacklist",
                   "extra.confidence": "low",
                   "extra.expires": "2019-02-03T20:12:03+00:00",
                   "source.fqdn": "example.com",
                   "extra.feed_source": "example",
                   "time.source": "2019-01-12T23:12:02+00:00",
                   "extra.feed_id": "some hex string",
                   "source.geolocation.cc": "AT",
                   "source.ip": "10.0.0.1",
                   "source.asn": 65536,
                   "raw": BLACKLIST_REPORT['raw']
                   }


class TestN6StompParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for N6StompParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = N6StompParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_blacklist(self):
        """ Test event of type "bl-update". """
        self.input_message = BLACKLIST_REPORT
        self.run_bot()
        self.assertMessageEqual(0, BLACKLIST_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
