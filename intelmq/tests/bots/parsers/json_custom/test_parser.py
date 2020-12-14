# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.json_custom.parser import JSONCustomParserBot

with open(os.path.join(os.path.dirname(__file__), 'sample.json'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

REPORT = {"feed.name": "RSTThreats URL Feed",
          "raw": RAW,
          "__type": "Report",
          }
EVENT = {'__type': 'Event',
         'classification.type': 'malware',
         'extra.tags': ['malware'],
         'extra.threat_info': [],
         'feed.name': 'RSTThreats URL Feed',
         'raw': 'eyJ1cmwiOiAiMTE0LjIzNC4xNjYuMjU1OjM5NDM2L21vemkuYSIsICJmc2VlbiI6IDE1OTg5MTg0MDA'
                'sICJsc2VlbiI6IDE2MDE5NDI0MDAsICJjb2xsZWN0IjogMTYwMjAyODgwMCwgInRhZ3MiOiB7InN0ci'
                'I6IFsibWFsd2FyZSJdLCAiY29kZXMiOiBbMTBdfSwgInNjb3JlIjogeyJ0b3RhbCI6IDEwLCAic3JjI'
                'jogNzMuMDYsICJ0YWdzIjogMC44OSwgImZyZXF1ZW5jeSI6IDAuNTh9LCAicmVzb2x2ZWQiOiB7InN0'
                'YXR1cyI6IDUwM30sICJmcCI6IHsiYWxhcm0iOiAidHJ1ZSIsICJkZXNjciI6ICJSZXNvdXJjZSB1bmF'
                '2YWlsYWJsZSJ9LCAidGhyZWF0IjogW10sICJpZCI6ICI5ODdmNTAzOC0yOThmLTM3ZWItYTFkNS1hMT'
                'cxMDVmNmI0YjUiLCAidGl0bGUiOiAiUlNUIFRocmVhdCBmZWVkLiBJT0M6IDExNC4yMzQuMTY2LjI1N'
                'TozOTQzNi9tb3ppLmEiLCAiZGVzY3JpcHRpb24iOiAiSU9DIHdpdGggdGFnczogbWFsd2FyZSJ9',
         'time.source': '2020-10-06T00:00:00+00:00',
         'source.url': 'http://114.234.166.255:39436/mozi.a'
         }


class TestJSONCustomParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a JSONCustomParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JSONCustomParserBot

    def test_sample(self):
        """ Test if correct Event has been produced. """
        self.input_message = REPORT
        self.sysconfig = {"splitlines": True,
                          "type": "malware",
                          "time_format": "epoch_millis",
                          "translate_fields": {"source.url": "url",
                                               "time.source": "lseen",
                                               "extra.tags": "tags.str",
                                               "extra.threat_info": "threat"
                                               }
                          }
        self.run_bot()
        self.assertMessageEqual(0, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
