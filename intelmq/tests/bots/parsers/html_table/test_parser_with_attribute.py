# -*- coding: utf-8 -*-
import datetime
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot


with open(os.path.join(os.path.dirname(__file__), 'html_table_with_attribute.data')) as handle:
    SAMPLE_FILE = handle.read()

THIS_YEAR = datetime.date.today().year
EXAMPLE_REPORT = {"feed.name": "HTML Table Feed",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 "classification.type": "malware",
                 "feed.name": "HTML Table Feed",
                 "malware.hash.md5": "A5144B1F31AAD413075FFBD9D91D4EB9",
                 "raw": "PHRyPgo8dGQgY2xhc3M9ImZvbmNlIj4wMi0xNTwvdGQ+Cjx0Z"
                        "CBjbGFzcz0iZm9uY2UiPmxpbmd2YXdvcmxkLnJ1L21lZGlhL3"
                        "N5c3RlbS9jc3MvbWVzc2cuanBnPC90ZD4KPHRkIGNsYXNzPSJ"
                        "mb25jZSI+QTUxNDRCMUYzMUFBRDQxMzA3NUZGQkQ5RDkxRDRF"
                        "Qjk8L3RkPgo8dGQgY2xhc3M9ImZvbmNlIj44MS4xNzcuMTM1L"
                        "jE3MsKgPC90ZD4KPC90cj4=",
                 "source.ip": "81.177.135.172",
                 "source.url": "http://lingvaworld.ru/media/system/css/messg.jpg",
                 "time.source": "%d-02-15T00:00:00+00:00" % THIS_YEAR}

EXAMPLE_EVENT1 = {"feed.name": "HTML Table Feed",
                  "__type": "Event",
                  "time.source": "2019-02-15T00:00:00+00:00",
                  "malware.name": "amadey",
                  "classification.type": "malware",
                  "source.ip": "51.15.130.100",
                  "source.url": "http://servicestatus.one/b2ccsaG/login.php",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  "raw": "PHRyPgo8dGQ+MTUtMDItMjAxOTwvdGQ+Cjx0ZD5zZXJ2aWNlc3"
                         "RhdHVzLm9uZS9iMmNjc2FHL2xvZ2luLnBocDwvdGQ+Cjx0ZD41M"
                         "S4xNS4xMzAuMTAwPC90ZD4KPHRkPkFtYWRleTwvdGQ+CjwvdHI+"}

EXAMPLE_EVENT2 = {"__type": "Event",
                  "classification.type": "malware",
                  "feed.name": "HTML Table Feed",
                  "raw": "PHRyPgo8dGQgc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7IHdvc"
                         "mQtd3JhcDpicmVhay13b3JkOyI+aHR0cDovL3d3dy5yeWFubW"
                         "90b3JzLmNvL2Jhbm5lcnMvb2JtL29ibS5leGU8L3RkPgo8dGQ"
                         "gc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7Ij4yMDE4LTExLTIy"
                         "IDAwOjMwOjA2CiAgICAgICAgPC90ZD4KPC90cj4=",
                  "source.url": "http://www.ryanmotors.co/banners/obm/obm.exe",
                  "time.source": "2018-11-22T00:30:06+00:00"}


@test.skip_exotic()
class TestHTMLTableParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a HTMLTableParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event_with_attribute_id(self):
        self.sysconfig = {"columns": ["time.source", "source.url",
                                      "malware.hash.md5", "source.ip"],
                          "skip_head": True,
                          "attribute_name": "id",
                          "attribute_value": "details",
                          "default_url_protocol": "http://",
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_event_with_attribute_class(self):
        self.sysconfig = {"columns": ["time.source", "source.url",
                                      "source.ip", "malware.name"],
                          "skip_head": True,
                          "default_url_protocol": "http://",
                          "attribute_name": "class",
                          "attribute_value": "ExploitTable",
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT1)

    def test_event_with_attribute_style(self):
        self.sysconfig = {"columns": ["source.url", "time.source"],
                          "skip_head": True,
                          "default_url_protocol": "http://",
                          "attribute_name": "style",
                          "attribute_value": "table-layout: fixed;",
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
