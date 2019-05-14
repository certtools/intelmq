# -*- coding: utf-8 -*-

import unittest
import os

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot

with open(os.path.join(os.path.dirname(__file__), 'data_type.csv')) as handle:
    SAMPLE_FILE = handle.read()
SAMPLE_SPLIT = SAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Sample CSV Feed",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00"}
EXAMPLE_EVENT = {"feed.name": "Sample CSV Feed",
                 "__type": "Event",
                 "raw": utils.base64_encode(SAMPLE_FILE.replace('\n', '\r\n')),
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "classification.type": "infected-system",
                 "source.ip": "11.11.11.11",
                 'extra.tags': ["t1", "t2", "t3"],
                 'source.url': 'http://test.com'}


class TestGenericCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a GenericCsvParserBot with extra, column_regex_search and windows_nt time format.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericCsvParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {"columns": [ "source.ip", "source.url", "extra.tags"],
                         "delimiter": ",",
                         "skip_header": True,
                         "type": "infected-system",
                         "data_type": "{\"extra.tags\":\"json\"}",
                        }
    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
