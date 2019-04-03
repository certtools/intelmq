# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot


with open(os.path.join(os.path.dirname(__file__), 'html_table_ignore_values.data')) as handle:
    SAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Feodo Tracker Browse",
                  "feed.url": "https://feodotracker.abuse.ch/browse",
                  "raw": utils.base64_encode(SAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "Feodo Tracker Browse",
                 "feed.url": "https://feodotracker.abuse.ch/browse",
                 "__type": "Event",
                 "time.source": "2019-02-06T10:36:27+00:00",
                 "malware.name": "heodo",
                 "classification.type": "malware",
                 "source.ip": "201.192.163.160",
                 "status": "Online",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 'source.as_name': 'AS11830 Instituto Costarricense de Electricidad y Telecom.',
                 'source.geolocation.cc': 'CR',

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

EXAMPLE_EVENT3 = {"feed.name": "Feodo Tracker Browse",
                 "feed.url": "https://feodotracker.abuse.ch/browse",
                 "__type": "Event",
                 "time.source": "2018-12-11T18:26:22+00:00",
                 "malware.name": "heodo",
                 "classification.type": "malware",
                 "source.ip": "179.33.30.194",
                 "status": "Offline",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 "extra.SBL": "SBL426579",
                 'source.as_name': 'AS3816 COLOMBIA TELECOMUNICACIONES S.A. ESP',
                 'source.geolocation.cc': 'CO',

                 'raw': 'PHRyPgo8dGQ+MjAxOC0xMi0xMSAxODoyNjoyMjwvdGQ+Cjx0ZD48YSBocmVmPSIvYnJvd3NlL2hvc3QvMTc5LjMzLjMwLjE5NC8iIHRhcmdldD0iX3BhcmVudCIgdGl0bGU9IkdldCBtb3JlIGluZm9ybWF0aW9uIGFib3V0IHRoaXMgYm90bmV0IEMmYW1wO0MiPjE3OS4zMy4zMC4xOTQ8L2E+PC90ZD4KPHRkPjxzcGFuIGNsYXNzPSJiYWRnZSBiYWRnZS1pbmZvIj5IZW9kbyA8YSBjbGFzcz0ibWFscGVkaWEiIGhyZWY9Imh0dHBzOi8vbWFscGVkaWEuY2FhZC5ma2llLmZyYXVuaG9mZXIuZGUvZGV0YWlscy93aW4uZ2VvZG8iIHRhcmdldD0iX2JsYW5rIiB0aXRsZT0iTWFscGVkaWE6IEdlb2RvIChha2EgRW1vdGV0IGFrYSBIZW9kbykiPjwvYT48L3NwYW4+PC90ZD4KPHRkPjxzcGFuIGNsYXNzPSJiYWRnZSBiYWRnZS1zdWNjZXNzIj5PZmZsaW5lPC9zcGFuPjwvdGQ+Cjx0ZD48YSBocmVmPSJodHRwczovL3d3dy5zcGFtaGF1cy5vcmcvc2JsL3F1ZXJ5L1NCTDQyNjU3OSIgdGFyZ2V0PSJfYmxhbmsiIHRpdGxlPSJTcGFtaGF1cyBTQkwgKFNCTDQyNjU3OSkiPjxzcGFuIGNsYXNzPSJiYWRnZSBiYWRnZS13YXJuaW5nIj5TQkw0MjY1Nzk8L3NwYW4+PC9hPjwvdGQ+Cjx0ZCBjbGFzcz0idGV4dC10cnVuY2F0ZSI+QVMzODE2IENPTE9NQklBIFRFTEVDT01VTklDQUNJT05FUyBTLkEuIEVTUDwvdGQ+Cjx0ZD48aW1nIGFsdD0iLSIgc3JjPSIvaW1hZ2VzL2ZsYWdzL2NvLnBuZyIgdGl0bGU9IkNPIi8+IENPPC90ZD48L3RyPg==',
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

    def test_event_with_ignore(self):
        """ Test if correct Event has been produced. """
        self.sysconfig = {"columns": ["time.source", "source.ip",
                                      "malware.name", "status", "extra.SBL",
                                      "source.as_name", "source.geolocation.cc"],
                          "ignore_values": ["", "", "", "", "Not listed", "", ""],
                          "skip_head": True,
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)
        self.assertMessageEqual(1, EXAMPLE_EVENT3)

    def test_event_without_ignore(self):
        """ Test if correct Event has been produced. """
        self.sysconfig = {"columns": ["time.source", "source.ip",
                                      "malware.name", "status", "extra.SBL",
                                      "source.as_name", "source.geolocation.cc"],
                          "skip_head": True,
                          "type": "malware"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
