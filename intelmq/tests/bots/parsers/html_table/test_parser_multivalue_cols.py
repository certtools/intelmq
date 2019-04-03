# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot


with open(os.path.join(os.path.dirname(__file__), 'html_table_multivalue_cols.data')) as handle:
    SAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Precisionsec Agent Tesla IOC Feed",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Precisionsec Agent Tesla IOC Feed",
                 "__type": "Event",
                 "time.source": "2018-11-22T00:30:06+00:00",
                 "classification.type": "malware",
                 "source.url": "http://www.ryanmotors.co/banners/obm/obm.exe",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 "raw": "PHRyPgo8dGQgc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7IHdvcmQtd3JhcDpicmVhay13b3JkO"
                        "yI+aHR0cDovL3d3dy5yeWFubW90b3JzLmNvL2Jhbm5lcnMvb2JtL29ibS5leGU8L3RkPgo8dG"
                        "Qgc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7Ij4yMDE4LTExLTIyIDAwOjMwOjA2CjwvdGQ+CjwvdHI+"
                 }

EXAMPLE_EVENT1 = {"feed.name": "Precisionsec Agent Tesla IOC Feed",
                  "__type": "Event",
                  "time.source": "2018-11-19T10:50:41+00:00",
                  "classification.type": "malware",
                  "source.ip": "192.185.143.150",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  "raw": "PHRyPgo8dGQgc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7IHdvcmQtd3JhcDpicmVhay13b3JkOy"
                         "I+MTkyLjE4NS4xNDMuMTUwPC90ZD4KPHRkIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0OyI+MjAx"
                         "OC0xMS0xOSAxMDo1MDo0MQo8L3RkPgo8L3RyPg=="
                  }


@test.skip_exotic()
class TestHTMLTableParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a HTMLTableParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {"columns": ["source.ip|source.url", "time.source"],
                         "type": "malware"}

    def test_event(self):
        """
        Test if correct Event has been produced.

        The row without data must be ignored.
        """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(1, EXAMPLE_EVENT1)
        self.assertOutputQueueLen(10)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
