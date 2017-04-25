# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.json.parser import JSONParserBot

ONELINE_REPORT = {"feed.name": "Test",
                  "raw": "eyJmZWVkLm5hbWUiOiAiVGVzdCBmZWVkIiwgInJhdyI6ICJabTl2WW1GeUNnPT0iLCAiX190eXBlIjogIkV2ZW50IiwgInRpbWUub2JzZXJ2YXRpb24iOiAiMjAxNS0wMS0wMVQwMDowMDowMCswMDowMCIsICJjbGFzc2lmaWNhdGlvbi50eXBlIjogInVua25vd24ifQ==",
                  "__type": "Report",
                  "time.observation": "2016-10-10T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Test feed",
                 "raw": "Zm9vYmFyCg==",
                 "__type": "Event",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "classification.type": "unknown"
                 }
with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

MULTILINE_REPORT = {"feed.name": "Test feed",
                    "raw": RAW,
                    "__type": "Report",
                    }
MULTILINE_EVENTS = [{"feed.name": "Test feed",
                     "raw": 'eyJfX3R5cGUiOiAiRXZlbnQiLCAic291cmNlLmlwIjogIjEyNy4wLjAuMSIsICJjbGFzc2lmaWNhdGlvbi50eXBlIjogImMmYyJ9',
                     "__type": "Event",
                     "classification.type": "c&c",
                     "source.ip": "127.0.0.1"
                     },
                    {"feed.name": "Test feed",
                     "raw": 'eyJfX3R5cGUiOiAiRXZlbnQiLCAic291cmNlLmlwIjogIjEyNy4wLjAuMiIsICJjbGFzc2lmaWNhdGlvbi50eXBlIjogImMmYyJ9',
                     "__type": "Event",
                     "classification.type": "c&c",
                     "source.ip": "127.0.0.2"
                     },
                    ]
with open(os.path.join(os.path.dirname(__file__), 'data2.json'), 'rb') as fh:
    RAW2 = base64.b64encode(fh.read()).decode()

NO_DEFAULT_REPORT = {"feed.name": "Test feed",
                     "raw": RAW2,
                     "__type": "Report",
                     }
NO_DEFAULT_EVENT = MULTILINE_EVENTS[1].copy()
NO_DEFAULT_EVENT['raw'] = 'eyJzb3VyY2UuaXAiOiAiMTI3LjAuMC4yIiwgImNsYXNzaWZpY2F0aW9uLnR5cGUiOiAiYyZjIn0K'


class TestJSONParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a MalwareDomainListParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JSONParserBot
        cls.default_input_message = ONELINE_REPORT

    def test_oneline_report(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_multiline_report(self):
        """ Test if correct Event has been produced. """
        self.input_message = MULTILINE_REPORT
        self.sysconfig = {"splitlines": True}
        self.run_bot()
        self.assertMessageEqual(0, MULTILINE_EVENTS[0])
        self.assertMessageEqual(1, MULTILINE_EVENTS[1])

    def test_default_event(self):
        """ Test if correct Event has been produced. """
        self.input_message = NO_DEFAULT_REPORT
        self.run_bot()
        self.assertMessageEqual(0, NO_DEFAULT_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
