# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.json_custom.parser import JSONCustomParserBot

with open(os.path.join(os.path.dirname(__file__), 'multiple_msg.json'), 'rb') as fh:
    RAW1 = base64.b64encode(fh.read()).decode()

MULTILINE_REPORT = {"feed.name": "RSTThreats Domain Feed",
                    "raw": RAW1,
                    "__type": "Report",
                    }

MULTIPLE_EVENT1 = {'__type': 'Event',
                   'classification.type': 'malware',
                   'extra.tags': ['spam'],
                   'extra.threat_info': [],
                   'feed.name': 'RSTThreats Domain Feed',
                   'raw': 'eyJkb21haW4iOiAia3JlZGl0b2huZXNjaHVmYTQ4LmRlIiwgImZzZWVuIjogMTU3NjM2O'
                          'DAwMCwgImxzZWVuIjogMTYwNzczMTIwMCwgImNvbGxlY3QiOiAxNjA3ODE3NjAwLCAidG'
                          'FncyI6IHsic3RyIjogWyJzcGFtIl0sICJjb2RlcyI6IFsyXX0sICJyZXNvbHZlZCI6IHs'
                          'iaXAiOiB7ImEiOiBbIjIzLjYwLjkxLjIyNSIsICIyMy4yMDAuMjM3LjIyNSJdLCAiYWxp'
                          'YXMiOiBbXSwgImNuYW1lIjogW119LCAid2hvaXMiOiB7ImNyZWF0ZWQiOiAiMTk3MC0wM'
                          'S0wMSAwMDowMDowMCIsICJ1cGRhdGVkIjogIjE5NzAtMDEtMDEgMDA6MDA6MDAiLCAiZX'
                          'hwaXJlcyI6ICIxOTcwLTAxLTAxIDAwOjAwOjAwIiwgImFnZSI6IDAsICJyZWdpc3RyYXI'
                          'iOiAidW5rbm93biIsICJyZWdpc3RyYW50IjogInVua25vd24iLCAiaGF2ZWRhdGEiOiAi'
                          'ZmFsc2UifX0sICJzY29yZSI6IHsidG90YWwiOiAzLCAic3JjIjogNjAuMiwgInRhZ3MiO'
                          'iAwLjc1LCAiZnJlcXVlbmN5IjogMC4wN30sICJmcCI6IHsiYWxhcm0iOiAiZmFsc2UiLC'
                          'AiZGVzY3IiOiAiIn0sICJ0aHJlYXQiOiBbXSwgImlkIjogImQyNjdjNjBmLTU3MDktMzY'
                          '5OC05NTIzLWY3MjdmNDJhYjVjNyIsICJ0aXRsZSI6ICJSU1QgVGhyZWF0IGZlZWQuIElP'
                          'Qzoga3JlZGl0b2huZXNjaHVmYTQ4LmRlIiwgImRlc2NyaXB0aW9uIjogIklPQyB3aXRoI'
                          'HRhZ3M6IHNwYW0ifQ==',
                   'source.fqdn': 'kreditohneschufa48.de',
                   'source.ip': '23.60.91.225',
                   'time.source': '2020-12-12T00:00:00+00:00'
                   }

MULTIPLE_EVENT2 = MULTIPLE_EVENT1.copy()
MULTIPLE_EVENT2["source.ip"] = "23.200.237.225"


class TestJSONCustomParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a JSONCustomParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JSONCustomParserBot

    def test_multiple_msg(self):
        """ Test if correct Event has been produced. """
        self.input_message = MULTILINE_REPORT
        self.sysconfig = {"splitlines": True,
                          "type": "malware",
                          "time_format": "epoch_millis",
                          "multiple_msg_field": "source.ip",
                          "translate_fields": {"source.fqdn": "domain",
                                               "time.source": "lseen",
                                               "extra.tags": "tags.str",
                                               "extra.threat_info": "threat",
                                               "source.ip": "resolved.ip.a"
                                               }
                          }
        self.run_bot()
        self.assertMessageEqual(0, MULTIPLE_EVENT1)
        self.assertMessageEqual(1, MULTIPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
