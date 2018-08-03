# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot


with open(os.path.join(os.path.dirname(__file__), 'invalid_sample_report.csv')) as handle:
    SAMPLE_FILE = handle.read()
SAMPLE_SPLIT = SAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Sample CSV Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Sample CSV Feed",
                 "__type": "Event",
                 "time.source": "2018-08-01T07:49:41+00:00",
                 "classification.type": "malware",
                 "source.ip": "127.0.0.1",
                 "source.fqdn": "example.com",
                 "raw": utils.base64_encode(SAMPLE_SPLIT[1]+'\r\n'),
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_EVENT2 = EXAMPLE_EVENT.copy()
del EXAMPLE_EVENT2['source.fqdn']
EXAMPLE_EVENT2["raw"] = utils.base64_encode(SAMPLE_SPLIT[0]+'\r\n')


class TestGenericCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a GenericCsvParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericCsvParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {"columns": ["time.source", "source.ip",
                                     "source.fqdn"],
                         "delimiter": ",",
                         "type": "malware",
                         "default_url_protocol": "http://"}

    def test_error(self):
        """ Test if the error is raised. """
        self.allowed_error_count = 1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertLogMatches("Failed to parse line.")
        self.assertLogMatches("intelmq.lib.exceptions.InvalidValue: invalid value '-' \(<class 'str'>\) for key 'source.fqdn'")

    def test_error_ignore(self):
        self.sysconfig = {"columns": ["time.source", "source.ip",
                                      "source.fqdn"],
                          "delimiter": ",",
                          "type": "malware",
                          "default_url_protocol": "http://",
                          "columns_required": [True, True, False],
                          }
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT2)
        self.assertMessageEqual(1, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
