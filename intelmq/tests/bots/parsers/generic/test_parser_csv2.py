# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot

EXAMPLE_REPORT = {"feed.name": "Sample CSV Feed",
                  "feed.url": "http://www.samplecsvthreatfeed.com/list",
                  "raw": "MjAxNi0xMi0xNCAwNDoxOTowMAlUZXN0aW5nCVJlYWxseSBiYWQgY"
                         "WN0b3Igc2l0ZSBjb21tZW50CU5vdGhpbmcJVW5pbXBvcnRhbnQJd3"
                         "d3LmNlbm5vd29ybGQuY29tL1BheW1lbnRfQ29uZmlybWF0aW9uL1B"
                         "heW1lbnRfQ29uZmlybWF0aW9uLnppcAkxOTguMTA1LjIyMS4xNjEJ"
                         "bWFpbDUuYnVsbHMudW5pc29ucGxhdGZvcm0uY29tCWp1c3QgYW5vd"
                         "GhlciBjb21tZW50",
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Sample CSV Feed",
                 "feed.url": "http://www.samplecsvthreatfeed.com/list",
                 "__type": "Event",
                 "time.source": "2016-12-14T04:19:00+00:00",
                 "source.url": "http://www.cennoworld.com/Payment_Confirmation/"
                               "Payment_Confirmation.zip",
                 "source.ip": "198.105.221.161",
                 "source.fqdn": "mail5.bulls.unisonplatform.com",
                 "event_description.text": "Really bad actor site comment",
                 "classification.type": "malware",
                 "raw": "MjAxNi0xMi0xNCAwNDoxOTowMCxUZXN0aW5nLFJlYWxseSBiYWQgYWN"
                        "0b3Igc2l0ZSBjb21tZW50LE5vdGhpbmcsVW5pbXBvcnRhbnQsd3d3Lm"
                        "Nlbm5vd29ybGQuY29tL1BheW1lbnRfQ29uZmlybWF0aW9uL1BheW1lb"
                        "nRfQ29uZmlybWF0aW9uLnppcCwxOTguMTA1LjIyMS4xNjEsbWFpbDUu"
                        "YnVsbHMudW5pc29ucGxhdGZvcm0uY29tLGp1c3QgYW5vdGhlciBjb21"
                        "tZW50DQo=",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }


class TestGenericCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a GenericCsvParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericCsvParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {"columns": ["time.source", "classification.type",
                                     "event_description.text", "__IGNORE__",
                                     "__IGNORE__", "source.url", "source.ip",
                                     "source.fqdn", "__IGNORE__"],
                         "delimiter": "\t",
                         "type_translation": "{\"Testing\": \"malware\"}",
                         "default_url_protocol": "http://"}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
