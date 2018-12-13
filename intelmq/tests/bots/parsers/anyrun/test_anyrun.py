# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.anyrun.parser import AnyrunParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_anyrun.data')) as handle:
    REPORT_DATA = handle.read()
    REPORT_DATA_SPLIT = REPORT_DATA.splitlines()

REPORT = {"__type": "Report",
          "feed.name": "Anyrun",
          "feed.url": "https://any.run/report/",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }
EVENT1 = {"raw": """ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD5vbWVnYWdvb2R3aW4uY29tPC
90ZD4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSIiPjUyLjAu
MTIzLjI0NSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGJyPiAgICAgIC
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPiAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICA8dGQ+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC
AgICA8c3BhbiBjbGFzcz0iYmFkZ2UgYmFkZ2UtZGFuZ2VyIj4gICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICBtYWxpY2lvdXM=""",
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "https://any.run/report/",
          "source.fqdn": "omegagoodwin.com",
          "classification.identifier": "macros, macros-on-open, generated-doc, trojan, loader, banker, emotet, feodo",
          "classification.type": "malware",
          "feed.accuracy": 80,
          "feed.name": "Anyrun"}

EVENT2 = {"raw": "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD5uaXRlY2NvcnAuY29tPC90ZD4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSIiPjY0LjExOC44NC40ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YnI+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJiYWRnZSBiYWRnZS1kYW5nZXIiPiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1hbGljaW91cw==",
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "https://any.run/report/",
          "source.fqdn": "niteccorp.com",
          "classification.identifier": "macros, macros-on-open, generated-doc, trojan, loader, banker, emotet, feodo",
          "classification.type": "malware",
          "feed.accuracy": 80,
          "feed.name": "Anyrun"}

EVENT3 = {"raw": 'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD5mdXR1cm9uLm5ldDwvdGQ+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZCBjbGFzcz0iIj4xOTMuMTg5LjEzOS4xMjkgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxicj4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIGJhZGdlLWRhbmdlciI+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbWFsaWNpb3Vz',
          "__type": "Event",
          "time.observation": "2018-01-22T14:38:24+00:00",
          "feed.url": "https://any.run/report/",
          "source.fqdn": "futuron.net",
          "classification.identifier": "macros, macros-on-open, generated-doc, trojan, loader, banker, emotet, feodo",
          "classification.type": "malware",
          "feed.accuracy": 80,
          "feed.name": "Anyrun"}


class TestAnyrunParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AnyrunParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':
    unittest.main()
