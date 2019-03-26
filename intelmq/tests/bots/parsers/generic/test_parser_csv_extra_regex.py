# -*- coding: utf-8 -*-

import unittest
import os

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot

with open(os.path.join(os.path.dirname(__file__), 'extra_regex.csv')) as handle:
    SAMPLE_FILE = handle.read()
SAMPLE_SPLIT = SAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Microsoft DCU Feed",
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
                 "extra.source.metro_code": '0',
                 "extra.source": "Microsoft-DCU",
                 "extra.http_request": "29|",
                 "destination.ip": "224.1.1.1",
                 "destination.port": 1604,
                 "feed.name": "Microsoft DCU Feed",
                 "malware.name": "b106-ceeinject",
                 "source.geolocation.cc": "AT",
                 "source.geolocation.latitude": 48.1,
                 "source.geolocation.longitude": 16.0,
                 "source.ip": "198.51.100.1",
                 "source.port": 2367,
                 "source.asn": 65536,
                 "time.source": "2017-03-25T23:59:43+00:00"
                 }
EXAMPLE_EVENT2 = {"feed.name": "Sample CSV Feed",
                  "__type": "Event",
                  "raw": utils.base64_encode(SAMPLE_SPLIT[0] + '\r\n' +
                                            SAMPLE_SPLIT[2].replace('"', '')+'\r\n'),
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "classification.type": "infected system",
                  "destination.ip": "224.1.1.2",
                  "destination.port": 80,
                  "extra.http_method": "POST",
                  "extra.source.postal_code": '1100',
                  "extra.http_version": "1.1",
                  "extra.http_host": "dcu-a-202.microsoftinternetsafety.net",
                  "extra.source.metro_code": '0',
                  "extra.http_request": "/file-34fd81-003.php",
                  "extra.source": "Microsoft-DCU",
                  "extra.http_referer": "null",
                  "extra.http_user_agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0;)",
                  "feed.name": "Microsoft DCU Feed",
                  "malware.name": "b54-config",
                  "source.geolocation.cc": "AT",
                  "source.geolocation.latitude": 48.2,
                  "source.geolocation.longitude": 16.0,
                  "source.geolocation.city": "Vienna",
                  "source.geolocation.region": "09",
                  "source.ip": "198.51.100.2",
                  "source.port": 35453,
                  "source.asn": 65536,
                  "time.source": "2017-03-26T00:00:41+00:00"
                  }


class TestGenericCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a GenericCsvParserBot with extra, column_regex_search and windows_nt time format.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericCsvParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {"columns": [ "source.ip", "time.source", "extra.source", "malware.name",
                                     "source.port", "source.asn", "source.geolocation.city",
                                     "source.geolocation.cc", "source.geolocation.latitude",
                                     "source.geolocation.longitude", "extra.source.metro_code",
                                     "extra.source.postal_code", "source.geolocation.region",
                                     "destination.ip", "destination.port", "extra.http_request",
                                     "extra.http_referer", "extra.http_user_agent",
                                     "extra.http_method", "extra.http_version", "extra.http_host"],
                         "delimiter": ",",
                         "skip_header": True,
                         "time_format": "windows_nt",
                         "type": "infected system",
                         "type_translation": None,
                         "column_regex_search": {"source.asn": "[0-9]+"}}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(1, EXAMPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
