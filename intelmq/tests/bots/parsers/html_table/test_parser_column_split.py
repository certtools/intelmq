# -*- coding: utf-8 -*-
import datetime
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot


with open(os.path.join(os.path.dirname(__file__), 'html_table_column_split.data')) as handle:
    SAMPLE_FILE = handle.read()

THIS_YEAR = datetime.date.today().year
EXAMPLE_REPORT = {"feed.name": "HTML Table Feed",
                  "feed.url": "http://vxvault.net/ViriList.php",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "HTML Table Feed",
                 "feed.url": "http://vxvault.net/ViriList.php",
                 "__type": "Event",
                 "source.url": "http://lingvaworld.ru/media/system/css/messg.jpg",
                 "time.source": "%d-02-15T00:00:00+00:00" % THIS_YEAR,
                 "classification.type": "malware",
                 "source.ip": "81.177.135.172",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 "malware.hash.md5": "A5144B1F31AAD413075FFBD9D91D4EB9",
                 "raw": "PHRyPgo8dGQgY2xhc3M9ImZvbmNlIj48YSBocmVmPSJWaXJpRmljaGUucGhwP0lEPTQwNDIxIj4wM"
                        "i0xNTwvYT48L3RkPgo8dGQgY2xhc3M9ImZvbmNlIj48YSBocmVmPSJmaWxlcy9BNTE0NEIxRjMxQU"
                        "FENDEzMDc1RkZCRDlEOTFENEVCOS56aXAiPltEXTwvYT4gPGEgaHJlZj0iVmlyaUZpY2hlLnBocD9"
                        "JRD00MDQyMSI+bGluZ3Zhd29ybGQucnUvbWVkaWEvc3lzdGVtL2Nzcy9tZXNzZy5qcGc8L2E+PC90"
                        "ZD4KPHRkIGNsYXNzPSJmb25jZSI+PGEgaHJlZj0iVmlyaUxpc3QucGhwP01ENT1BNTE0NEIxRjMxQ"
                        "UFENDEzMDc1RkZCRDlEOTFENEVCOSI+QTUxNDRCMUYzMUFBRDQxMzA3NUZGQkQ5RDkxRDRFQjk8L2"
                        "E+PC90ZD4KPHRkIGNsYXNzPSJmb25jZSI+PGEgaHJlZj0iVmlyaUxpc3QucGhwP0lQPTgxLjE3Ny4"
                        "xMzUuMTcyIj44MS4xNzcuMTM1LjE3MjwvYT7CoDwvdGQ+Cjx0ZCBjbGFzcz0iZm9uY2UiPjxhIGhy"
                        "ZWY9Imh0dHA6Ly9wZWR1bXAubWUvYTUxNDRiMWYzMWFhZDQxMzA3NWZmYmQ5ZDkxZDRlYjkiPlBFR"
                        "DwvYT4KPGEgaHJlZj0iaHR0cDovL3VybHF1ZXJ5Lm5ldC9zZWFyY2g/cT04MS4xNzcuMTM1LjE3Mi"
                        "I+VVE8L2E+CjwvdGQ+CjwvdHI+"}

EXAMPLE_EVENT2 = EXAMPLE_EVENT.copy()
EXAMPLE_EVENT2['source.url'] = "http://[D] lingvaworld.ru/media/system/css/messg.jpg"


@test.skip_exotic()
class TestHTMLTableParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a HTMLTableParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event_with_split(self):
        self.sysconfig = {"columns": ["time.source", "source.url", "malware.hash.md5",
                                      "source.ip", "__IGNORE__"],
                          "skip_head": True,
                          "default_url_protocol": "http://",
                          "split_column": "source.url",
                          "split_separator": "[D]",
                          "split_index": "1",
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_event_without_split(self):
        self.sysconfig = {"columns": ["time.source", "source.url", "malware.hash.md5",
                                      "source.ip", "__IGNORE__"],
                          "skip_head": True,
                          "default_url_protocol": "http://",
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
