# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot


with open(os.path.join(os.path.dirname(__file__), 'html_table.data')) as handle:
    SAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "HTML Table Feed",
                  "feed.url": "https://cybercrime-tracker.net/index.php",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "HTML Table Feed",
                 "feed.url": "https://cybercrime-tracker.net/index.php",
                 "__type": "Event",
                 "time.source": "2019-02-15T00:00:00+00:00",
                 "malware.name": "amadey",
                 "classification.type": "malware",
                 "source.ip": "51.15.130.100",
                 "source.url": "http://servicestatus.one/b2ccsaG/login.php",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 "raw": "PHRyPjx0ZD4xNS0wMi0yMDE5PC90ZD4KPHRkPnNlcnZpY2VzdGF0dXMub25lL2IyY2NzYUcvbG9"
                        "naW4ucGhwPC90ZD4KPHRkPjxhIGhyZWY9Imh0dHBzOi8vd3d3LnZpcnVzdG90YWwuY29tL2VuL2"
                        "lwLWFkZHJlc3MvNTEuMTUuMTMwLjEwMC9pbmZvcm1hdGlvbi8iIHRhcmdldD0iX2JsYW5rIj41M"
                        "S4xNS4xMzAuMTAwPC9hPjwvdGQ+Cjx0ZD5BbWFkZXk8L3RkPgo8dGQ+PGEgaHJlZj0iaHR0cHM6"
                        "Ly93d3cudmlydXN0b3RhbC5jb20vbGF0ZXN0LXNjYW4vaHR0cDovL3NlcnZpY2VzdGF0dXMub25"
                        "lL2IyY2NzYUcvbG9naW4ucGhwIiB0YXJnZXQ9Il9ibGFuayI+PGltZyBib3JkZXI9IjAiIGhlaW"
                        "dodD0iMTIiIHNyYz0idnQucG5nIiB0aXRsZT0iU2NhbiB3aXRoIFZpcnVzVG90YWwiIHdpZHRoP"
                        "SIxMyIvPjwvYT4gPGEgaHJlZj0iaHR0cDovL2N5YmVyY3JpbWUtdHJhY2tlci5uZXQvaW5kZXgu"
                        "cGhwP3M9MCZhbXA7bT00MCZhbXA7c2VhcmNoPUFtYWRleSI+PGltZyBib3JkZXI9IjAiIGhlaWd"
                        "odD0iMTIiIHNyYz0idndpY24wMDguZ2lmIiB0aXRsZT0iU2VhcmNoIHRoZSBmYW1pbHkiIHdpZH"
                        "RoPSIxMyIvPjwvYT48L3RkPjwvdHI+"
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
        cls.sysconfig = {"columns": ["time.source", "source.url", "source.ip",
                                     "malware.name", "__IGNORE__"],
                         "skip_head": True,
                         "default_url_protocol": "http://",
                         "type": "malware"}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
