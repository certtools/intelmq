# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.n6.parser_n6stomp import N6StompParserBot

EXAMPLE_REPORT = {"feed.name": "n6stomp",
                  "raw": "eyJjYXRlZ29yeSI6ICJib3RzIiwgIm9yaWdpbiI6ICJzaW5raG9sZSIsICJjb25maWRlbmNlIjogImhpZ2giLCAibmFtZSI6ICJzYWxpdHkiLCAicHJvdG8iOiAidGNwIiwgImFkZHJlc3MiOiBbeyJjYyI6ICJVUyIsICJpcCI6ICI2OC42OC45Ni4yMzUiLCAiYXNuIjogMTg3Nzl9XSwgInNvdXJjZSI6ICJjZXJ0LXBsLnNpbmtob2xlIiwgImFkaXAiOiAieC54LjExMS45OSIsICJ0aW1lIjogIjIwMTUtMTEtMTdUMTI6MTc6MjcuMDQzNDUyWiIsICJkcG9ydCI6IDgwLCAic3BvcnQiOiAyMjMwOCwgInR5cGUiOiAiZXZlbnQiLCAiaWQiOiAiZDc3YWU4Y2Y2ODFkY2RiYjZlMjAwMTQ1ODE0MDFlZDUifQ==",  # noqa
                  "__type": "Report",
                  "time.observation": "2015-11-17T12:17:27.043452Z",
                  "feed.url": "stomp://n6stream.cert.pl:61614//exchange/cert.at/#"
                  }
EXAMPLE_EVENT = {"feed.name": "n6stomp",
                 "source.ip": "68.68.96.235",
                 "time.source": "2015-11-17T12:17:27.043452+00:00",
                 "classification.taxonomy": "malicious code",
                 "extra": '{"adip": "x.x.111.99", "feed_id": "d77ae8cf681dcdbb6e20014581401ed5"}',
                 "source.port": 22308,
                 "time.observation": "2015-11-17T12:17:27.043452Z",
                 "source.geolocation.cc": "US",
                 "raw": "eyJjYXRlZ29yeSI6ICJib3RzIiwgIm9yaWdpbiI6ICJzaW5raG9sZSIsICJjb25maWRlbmNlIjogImhpZ2giLCAibmFtZSI6ICJzYWxpdHkiLCAicHJvdG8iOiAidGNwIiwgImFkZHJlc3MiOiBbeyJjYyI6ICJVUyIsICJpcCI6ICI2OC42OC45Ni4yMzUiLCAiYXNuIjogMTg3Nzl9XSwgInNvdXJjZSI6ICJjZXJ0LXBsLnNpbmtob2xlIiwgImFkaXAiOiAieC54LjExMS45OSIsICJ0aW1lIjogIjIwMTUtMTEtMTdUMTI6MTc6MjcuMDQzNDUyWiIsICJkcG9ydCI6IDgwLCAic3BvcnQiOiAyMjMwOCwgInR5cGUiOiAiZXZlbnQiLCAiaWQiOiAiZDc3YWU4Y2Y2ODFkY2RiYjZlMjAwMTQ1ODE0MDFlZDUifQ==",  # noqa
                 "classification.identifier": "sality",
                 "malware.name": "sality",
                 "classification.type": "botnet drone",
                 "destination.port": 80,
                 "__type": "Event",
                 "protocol.transport": "tcp",
                 "source.asn": 18779,
                 "feed.url": "stomp://n6stream.cert.pl:61614//exchange/cert.at/#"
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


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
