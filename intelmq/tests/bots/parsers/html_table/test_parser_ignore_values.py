# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot


with open(os.path.join(os.path.dirname(__file__), 'html_table_ignore_values.data')) as handle:
    SAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "HTML Table Feed",
                  "feed.url": "https://feodotracker.abuse.ch/browse",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "HTML Table Feed",
                 "feed.url": "https://feodotracker.abuse.ch/browse",
                 "__type": "Event",
                 "time.source": "2019-02-06T10:36:27+00:00",
                 "malware.name": "heodo",
                 "classification.type": "malware",
                 "source.ip": "201.192.163.160",
                 "status": "Online",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 "raw": "PHRyPgo8dGQ+MjAxOS0wMi0wNiAxMDozNjoyNzwvdGQ+Cjx0ZD48YSBocmVmPSIvY"
                        "nJvd3NlL2hvc3QvMjAxLjE5Mi4xNjMuMTYwLyIgdGFyZ2V0PSJfcGFyZW50IiB0aX"
                        "RsZT0iR2V0IG1vcmUgaW5mb3JtYXRpb24gYWJvdXQgdGhpcyBib3RuZXQgQyZhbXA"
                        "7QyI+MjAxLjE5Mi4xNjMuMTYwPC9hPjwvdGQ+Cjx0ZD48c3BhbiBjbGFzcz0iYmFk"
                        "Z2UgYmFkZ2UtaW5mbyI+SGVvZG8gPGEgY2xhc3M9Im1hbHBlZGlhIiBocmVmPSJod"
                        "HRwczovL21hbHBlZGlhLmNhYWQuZmtpZS5mcmF1bmhvZmVyLmRlL2RldGFpbHMvd2"
                        "luLmdlb2RvIiB0YXJnZXQ9Il9ibGFuayIgdGl0bGU9Ik1hbHBlZGlhOiBHZW9kbyA"
                        "oYWthIEVtb3RldCBha2EgSGVvZG8pIj48L2E+PC9zcGFuPjwvdGQ+Cjx0ZD48c3Bh"
                        "biBjbGFzcz0iYmFkZ2UgYmFkZ2UtZGFuZ2VyIj48aW1nIGFsdD0iLSIgc3JjPSIva"
                        "W1hZ2VzL2ljb25zL2ZsYW1lLnN2ZyIvPiAgT25saW5lPC9zcGFuPjwvdGQ+Cjx0ZD"
                        "5Ob3QgbGlzdGVkPC90ZD4KPHRkIGNsYXNzPSJ0ZXh0LXRydW5jYXRlIj5BUzExODM"
                        "wIEluc3RpdHV0byBDb3N0YXJyaWNlbnNlIGRlIEVsZWN0cmljaWRhZCB5IFRlbGVj"
                        "b20uPC90ZD4KPHRkPjxpbWcgYWx0PSItIiBzcmM9Ii9pbWFnZXMvZmxhZ3MvY3Iuc"
                        "G5nIiB0aXRsZT0iQ1IiLz4gQ1I8L3RkPgo8L3RyPg=="
                 }

EXAMPLE_EVENT2 = EXAMPLE_EVENT.copy()
EXAMPLE_EVENT2['extra.SBL'] = "Not listed"


class TestHTMLTableParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a HTMLTableParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event_with_ignore(self):
        """ Test if correct Event has been produced. """
        self.sysconfig = {"columns": ["time.source", "source.ip",
                                      "malware.name", "status", "extra.SBL"],
                          "ignore_values": ["", "", "", "", "Not listed"],
                          "skip_head": True,
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_event_without_ignore(self):
        """ Test if correct Event has been produced. """
        self.sysconfig = {"columns": ["time.source", "source.ip",
                                      "malware.name", "status", "extra.SBL"],
                          "skip_head": True,
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
