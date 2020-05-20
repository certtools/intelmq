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
                 "classification.type": "infected-system",
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
NO_ADDRESS_REPORT = {"__type": "Report",
                     "time.observation": "2015-11-17T12:17:27.043452Z",
                     "raw": utils.base64_encode("""
{"category": "cnc", "confidence": "medium", "name": "some name", "fqdn": "secao.org", "source": "hidden.64534", "time": "2018-09-26T08:05:19Z", "type": "event", "id": "14758f1afd44c09b7992073ccf00b43d"}
""")}
NO_ADDRESS_EVENT = {"__type": "Event",
                    "time.observation": "2015-11-17T12:17:27.043452Z",
                    "extra.confidence": "medium",
                    "extra.feed_id": "14758f1afd44c09b7992073ccf00b43d",
                    "time.source": "2018-09-26T08:05:19+00:00",
                    "malware.name": "some name",
                    'classification.identifier': 'c&c server',
                    'classification.taxonomy': 'malicious code',
                    'classification.type': 'c2server',
                    'extra.feed_source': 'hidden.64534',
                    'source.fqdn': 'secao.org',
                    "raw": NO_ADDRESS_REPORT['raw']}
FURTHER_IOCS_REPORT = {"__type": "Report",
                       "time.observation": "2015-11-17T12:17:27.043452Z",
                       "raw": utils.base64_encode("""
{"category": "cnc", "confidence": "medium", "name": "further iocs: text with invalid ’ char", "url": "http://example.net", "fqdn": "example.net", "source": "hidden", "time": "2020-05-04T10:54:15Z", "type": "event", "id": "2f3db54a45039180d452b73d780e5bed"}
""")}
FURTHER_IOCS_EVENT = {"__type": "Event",
                      "time.observation": "2015-11-17T12:17:27.043452Z",
                      "extra.confidence": "medium",
                      "extra.feed_id": "2f3db54a45039180d452b73d780e5bed",
                      "time.source": "2020-05-04T10:54:15+00:00",
                      "malware.name": "further iocs: text with invalid  char",
                      "event_description.text": "further iocs: text with invalid ’ char",
                      'classification.identifier': 'c&c server',
                      'classification.taxonomy': 'malicious code',
                      'classification.type': 'c2server',
                      'extra.feed_source': 'hidden',
                      'source.fqdn': 'example.net',
                      'source.url': 'http://example.net',
                      "raw": FURTHER_IOCS_REPORT['raw']}



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

    def test_no_address(self):
        """ Test event without address. """
        self.input_message = NO_ADDRESS_REPORT
        self.run_bot()
        self.assertMessageEqual(0, NO_ADDRESS_EVENT)

    def test_futher_ios(self):
        """ Test an event with "further iocs"""
        self.input_message = FURTHER_IOCS_REPORT
        self.run_bot()
        self.assertMessageEqual(0, FURTHER_IOCS_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
