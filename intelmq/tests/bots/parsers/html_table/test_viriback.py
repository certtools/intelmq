# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_viriback.data')) as handle:
    REPORT_DATA = handle.read()
    IOCS = REPORT_DATA.splitlines()[78].strip()[8:-10].split("</td></tr><tr><td>")


REPORT = {"__type": "Report",
          "feed.name": "Viriback",
          "feed.url": "http://tracker.viriback.com/",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }


EVENT1 = {"raw": "PHRyPjx0ZD5Mb2tpYm90PC90ZD48dGQ+YWNwdHcuaWN1L2NsYXAvZml2ZS9QdnFEcTkyOUJTeF9BX0RfTTFuX2EucGhwPC90ZD48dGQ+NjIuMTczLjE0MC4xOTA8L3RkPjx0ZD4yMS0wNi0yMDE5PC90ZD48L3RyPg==",
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "time.source": "2019-06-21T00:00:00+00:00",
          "feed.url": "http://tracker.viriback.com/",
          "source.url": "http://acptw.icu/clap/five/PvqDq929BSx_A_D_M1n_a.php",
          "source.ip": "62.173.140.190",
          "classification.type": "malware",
          "malware.name": "lokibot",
          "feed.name": "Viriback"}

EVENT2 = {"raw": "PHRyPjx0ZD5Mb2tpYm90PC90ZD48dGQ+aXZhbmRhcmluYS50b3AvamFtL1B2cURxOTI5QlN4X0FfRF9NMW5fYS5waHA8L3RkPjx0ZD4xOTguMjMuMjEzLjExNDwvdGQ+PHRkPjIxLTA2LTIwMTk8L3RkPjwvdHI+",
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "time.source": "2019-06-21T00:00:00+00:00",
          "feed.url": "http://tracker.viriback.com/",
          "source.url": "http://ivandarina.top/jam/PvqDq929BSx_A_D_M1n_a.php",
          "source.ip": "198.23.213.114",
          "classification.type": "malware",
          "malware.name": "lokibot",
          "feed.name": "Viriback"}

EVENT3 = {"raw": "PHRyPjx0ZD5Mb2tpYm90PC90ZD48dGQ+YWRhbXNqZWYudG9wL2plZi9QdnFEcTkyOUJTeF9BX0RfTTFuX2EucGhwPC90ZD48dGQ+MTk4LjIzLjIxMy4xMTQ8L3RkPjx0ZD4yMS0wNi0yMDE5PC90ZD48L3RyPg==",
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "time.source": "2019-06-21T00:00:00+00:00",
          "feed.url": "http://tracker.viriback.com/",
          "source.url": "http://adamsjef.top/jef/PvqDq929BSx_A_D_M1n_a.php",
          "source.ip": "198.23.213.114",
          "classification.type": "malware",
          "malware.name": "lokibot",
          "feed.name": "Viriback"}


@test.skip_exotic()
class TestHTMLTableParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableParserBot
        cls.default_input_message = REPORT
        cls.sysconfig = {'columns': ['malware.name',
                                     'source.url',
                                     'source.ip',
                                     'time.source'],
                          'type': 'malware',
                          'time_format': 'from_format_midnight|%d-%m-%Y',
                          'html_parser': 'lxml',
                          }

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
