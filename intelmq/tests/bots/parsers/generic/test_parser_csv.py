# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot


with open(os.path.join(os.path.dirname(__file__), 'sample_report.csv')) as handle:
    SAMPLE_FILE = handle.read()
SAMPLE_SPLIT = SAMPLE_FILE.splitlines()
with open(os.path.join(os.path.dirname(__file__), 'compose_fields.csv')) as handle:
    COMPOSE_FILE = handle.read()
COMPOSE_SPLIT = COMPOSE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "Sample CSV Feed",
                  "feed.url": "http://www.samplecsvthreatfeed.com/list",
                  "raw": utils.base64_encode(SAMPLE_FILE),
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
                 "raw": utils.base64_encode(SAMPLE_SPLIT[10].replace('\t', ',')+'\r\n'),
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_EVENT2 = EXAMPLE_EVENT.copy()
EXAMPLE_EVENT2['time.source'] = "2016-12-14T04:19:00+00:00"
EXAMPLE_EVENT2['source.ip'] = "198.105.221.161"
EXAMPLE_EVENT2["raw"] = utils.base64_encode(SAMPLE_SPLIT[11].replace('\t', ',')+'\r\n')
COMPOSE_REPORT = {"feed.name": "Sample CSV Feed",
                  "raw": utils.base64_encode(COMPOSE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
COMPOSE_EVENT = {"feed.name": "Sample CSV Feed",
                 "__type": "Event",
                 "source.urlpath": "/foo/",
                 "source.url": "http://example.com/foo/",
                 "source.fqdn": "example.com",
                 "classification.type": "malware",
                 "raw": utils.base64_encode(COMPOSE_SPLIT[1]+'\r\n'),
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
        cls.sysconfig = {"columns": ["time.source", "__IGNORE__",
                                     "event_description.text", "__IGNORE__",
                                     "__IGNORE__", "source.url", "source.ip",
                                     "source.fqdn", "__IGNORE__"],
                         "delimiter": "\t",
                         "type": "malware",
                         "default_url_protocol": "http://"}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(1, EXAMPLE_EVENT2)

    def test_strcol(self):
        self.run_bot(parameters={"columns": "time.source, __IGNORE__,"
                                            "event_description.text, __IGNORE__,"
                                            "__IGNORE__, source.url, source.ip,"
                                            "source.fqdn, __IGNORE__",
                                 "delimiter": "\t",
                                 "type": "malware",
                                 "column_regex_search": "",
                                 "type_translation": "",
                                 "default_url_protocol": "http://"})
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(1, EXAMPLE_EVENT2)

    def test_compose_fields(self):
        self.input_message = COMPOSE_REPORT
        self.run_bot(parameters={'columns': ['source.fqdn', 'source.urlpath'],
                                 'compose_fields': {"source.url": "http://{0}{1}"},
                                 'delimiter': ','})
        self.assertMessageEqual(0, COMPOSE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
