# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.json.parser import JSONParserBot

EXAMPLE_REPORT = {"feed.name": "Test",
                  "raw": "eyJmZWVkLm5hbWUiOiAiVGVzdCBmZWVkIiwgInJhdyI6ICJabTl2WW1GeUNnPT0iLCAiX190eXBl"
                  "IjogIkV2ZW50IiwgInRpbWUub2JzZXJ2YXRpb24iOiAiMjAxNS0wMS0wMVQwMDowMDowMCswMDow"
                  "MCIsICJjbGFzc2lmaWNhdGlvbi50eXBlIjogInVua25vd24ifQ==",
                  "__type": "Report",
                  "time.observation": "2016-10-10T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Test feed",
                 "raw": "Zm9vYmFyCg==",
                 "__type": "Event",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "classification.type": "unknown"
                 }


class TestJSONParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a MalwareDomainListParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JSONParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_report(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
