# -*- coding: utf-8 -*-

import unittest
import os

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot

with open(os.path.join(os.path.dirname(__file__), 'empty_src_url.csv')) as handle:
    SAMPLE_FILE = handle.read()
SAMPLE_SPLIT = SAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Sample CSV Feed",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Sample CSV Feed",
                 "__type": "Event",
                 "raw": utils.base64_encode(SAMPLE_SPLIT[0] + '\r\n' +
                                            SAMPLE_SPLIT[1].replace('"', '')+'\r\n'),
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "classification.type": "infected system",
                 "source.ip": "11.11.11.11",
                 "feed.name": "Sample CSV Feed",
                 "source.port": 9001,
                 'time.source': '2017-05-26T07:00:36+00:00',
                 "source.url": "http://test.com"
                 }

EXAMPLE_EVENT2 = {"feed.name": "Sample CSV Feed",
                 "__type": "Event",
                 "raw": utils.base64_encode(SAMPLE_SPLIT[0] + '\r\n' +
                                            SAMPLE_SPLIT[2].replace('"', '')+'\r\n'),
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "classification.type": "infected system",
                 "source.ip": "11.11.11.11",
                 "feed.name": "Sample CSV Feed",
                 'time.source': '2017-05-26T07:00:37+00:00',
                 "source.port": 9001
                 }

EXAMPLE_EVENT3 = {"feed.name": "Sample CSV Feed",
                 "__type": "Event",
                 "raw": utils.base64_encode(SAMPLE_SPLIT[0] + '\r\n' +
                                            SAMPLE_SPLIT[3].replace('"', '')+'\r\n'),
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "classification.type": "infected system",
                 "source.ip": "11.11.11.11",
                 "feed.name": "Sample CSV Feed",
                 "source.port": 9001,
                 'time.source': '2017-05-26T07:00:38+00:00',
                 "source.url": "http://test.com"
                 }


class TestGenericCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a GenericCsvParserBot with extra, column_regex_search and windows_nt time format.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericCsvParserBot
        cls.default_input_message = EXAMPLE_REPORT
#source_ip,source_url,source_port
        cls.sysconfig = {"columns": [ "source.ip", "source.url", "source.port", "time.source" ],
                         "delimiter": ",",
                         "skip_header": True,
                         "type": "infected system",
                         "time_format": "epoch_millis",
                         "default_url_protocol": "http://",
                         "type_translation": None}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(1, EXAMPLE_EVENT2)
        self.assertMessageEqual(2, EXAMPLE_EVENT3)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
