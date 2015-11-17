# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.n6.parser_n6stomp import N6StompParserBot

EXAMPLE_REPORT = {"feed.name": "n6stomp",
                  "feed.url": "http://vxvault.siri-urz.net/URL_List.php",
                  "raw": "eyJjYXRlZ29yeSI6ICJib3RzIiwgIm9yaWdpbiI6ICJzaW5raG9sZSIsICJjb25maWRlbmNlIjogImhpZ2giLCAibmFtZSI6ICJzYWxpdHkiLCAicHJvdG8iOiAidGNwIiwgImFkZHJlc3MiOiBbeyJjYyI6ICJVUyIsICJpcCI6ICI2OC42OC45Ni4yMzUiLCAiYXNuIjogMTg3Nzl9XSwgInNvdXJjZSI6ICJjZXJ0LXBsLnNpbmtob2xlIiwgImFkaXAiOiAieC54LjExMS45OSIsICJ0aW1lIjogIjIwMTUtMTEtMTdUMTI6MTc6MjcuMDQzNDUyWiIsICJkcG9ydCI6IDgwLCAic3BvcnQiOiAyMjMwOCwgInR5cGUiOiAiZXZlbnQiLCAiaWQiOiAiZDc3YWU4Y2Y2ODFkY2RiYjZlMjAwMTQ1ODE0MDFlZDUifQ==",
                  "__type": "Report",
                  "time.observation": "2015-11-17T12:17:27.043452Z"
                  }
EXAMPLE_EVENT = {"feed.name": "n6stomp",
                 "feed.url": "stomp://n6stream.cert.pl:61614//exchange/cert.at/#",
                 "source.url": "http://example.com/bad/program.exe",
                 "classification.type": "malware",
                 "__type": "Event",
                 "time.observation": "2015-11-17T12:17:27.043452Z",
                 "raw": "eyJjYXRlZ29yeSI6ICJib3RzIiwgIm9yaWdpbiI6ICJzaW5raG9sZSIsICJjb25maWRlbmNlIjogImhpZ2giLCAibmFtZSI6ICJzYWxpdHkiLCAicHJvdG8iOiAidGNwIiwgImFkZHJlc3MiOiBbeyJjYyI6ICJVUyIsICJpcCI6ICI2OC42OC45Ni4yMzUiLCAiYXNuIjogMTg3Nzl9XSwgInNvdXJjZSI6ICJjZXJ0LXBsLnNpbmtob2xlIiwgImFkaXAiOiAieC54LjExMS45OSIsICJ0aW1lIjogIjIwMTUtMTEtMTdUMTI6MTc6MjcuMDQzNDUyWiIsICJkcG9ydCI6IDgwLCAic3BvcnQiOiAyMjMwOCwgInR5cGUiOiAiZXZlbnQiLCAiaWQiOiAiZDc3YWU4Y2Y2ODFkY2RiYjZlMjAwMTQ1ODE0MDFlZDUifQ=="
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
        print self.get_output_queue()
        print self.get_output_queue()[0]
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
