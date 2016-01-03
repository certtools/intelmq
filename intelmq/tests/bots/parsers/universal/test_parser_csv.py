# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.universal.parser_csv import \
    UniversalCsvParserBot

EXAMPLE_REPORT = {"feed.name": "Sample CSV Feed",
                  "feed.url": "http://www.samplecsvthreatfeed.com/list",
                  "raw": "MjAxNS0xMi0xNCAwNDoxOTowMAlUZXN0aW5nCVJlYWxseSBiYWQgY"
                         "WN0b3Igc2l0ZSBjb21tZW50CU5vdGhpbmcJVW5pbXBvcnRhbnQJd3"
                         "d3LmNlbm5vd29ybGQuY29tL1BheW1lbnRfQ29uZmlybWF0aW9uL1B"
                         "heW1lbnRfQ29uZmlybWF0aW9uLnppcAkxOTguMTA1LjIyMS41Ojgw"
                         "CW1haWw1LmJ1bGxzLnVuaXNvbnBsYXRmb3JtLmNvbQlqdXN0IGFub"
                         "3RoZXIgY29tbWVudA==",
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Sample CSV Feed",
                 "feed.url": "http://www.samplecsvthreatfeed.com/list",
                 "__type": "Event",
                 "time.source": "2015-12-14T04:19:00+00:00",
                 "source.url": "http://www.cennoworld.com/Payment_Confirmation/"
                               "Payment_Confirmation.zip",
                 "source.ip": "198.105.221.5",
                 "source.fqdn": "mail5.bulls.unisonplatform.com",
                 "event_description.text": "Really bad actor site comment",
                 "classification.type": "malware",
                 "raw": "MjAxNS0xMi0xNCAwNDoxOTowMCxUZXN0aW5nLFJlYWxseSBiYWQgYW"
                        "N0b3Igc2l0ZSBjb21tZW50LE5vdGhpbmcsVW5pbXBvcnRhbnQsd3d3"
                        "LmNlbm5vd29ybGQuY29tL1BheW1lbnRfQ29uZmlybWF0aW9uL1BheW"
                        "1lbnRfQ29uZmlybWF0aW9uLnppcCwxOTguMTA1LjIyMS41OjgwLG1h"
                        "aWw1LmJ1bGxzLnVuaXNvbnBsYXRmb3JtLmNvbSxqdXN0IGFub3RoZX"
                        "IgY29tbWVudA==",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }


class TestUniversalCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a UniversalCsvParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = UniversalCsvParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {"columns": ["time.source", "__IGNORE__",
                                     "event_description.text", "__IGNORE__",
                                     "__IGNORE__", "source.url", "source.ip",
                                     "source.fqdn", "__IGNORE__"],
                         "delimiter": "\t",
                         "type": "malware"}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
