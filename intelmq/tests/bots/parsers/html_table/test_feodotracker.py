# SPDX-FileCopyrightText: 2021 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import codecs
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.html_table.parser import HTMLTableParserBot
from intelmq.lib import utils

with codecs.open(os.path.join(os.path.dirname(__file__), 'feodotracker.html'), encoding='UTF-8') as handle:
    REPORT_DATA = handle.read()
REPORT_LINES = REPORT_DATA.splitlines()


REPORT = {"__type": "Report",
          "raw": utils.base64_encode(REPORT_DATA),
          }


line1 = '%s/%s' % (REPORT_LINES[94][:-14], REPORT_LINES[94][-14:])
EVENT1 = {"raw": utils.base64_encode(line1.strip()),
          "__type": "Event",
          "time.source": "2021-05-10T14:56:05+00:00",
          "source.ip": "94.177.255.18",
          "source.as_name": "AS199883 ARUBACLOUDLTD-ASN",
          "classification.type": "c2-server",
          "malware.name": "dridex",
          "source.geolocation.cc": "GB",
          "status": "Online",
          }
line2 = '%s/%s' % (REPORT_LINES[95][:-14], REPORT_LINES[95][-14:])
EVENT2 = {"raw": utils.base64_encode(line2.strip()),
          "__type": "Event",
          "time.source": "2021-05-10T14:56:04+00:00",
          "source.ip": "203.114.109.124",
          "source.as_name": "AS131293 TOT-LLI-AS-AP TOT Public Company Limited",
          "classification.type": "c2-server",
          "malware.name": "dridex",
          "source.geolocation.cc": "TH",
          "status": "Offline",
          }


@test.skip_exotic()
class TestHTMLTableParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableParserBot
        cls.default_input_message = REPORT
        cls.sysconfig = {'columns': 'time.source,source.ip,malware.name,status,source.as_name,source.geolocation.cc',
                         'type': 'c2-server',
                         'ignore_values': ',,,,,',
                         'skip_table_head': True,
                         }

    def test_event(self):
        print(REPORT_LINES[94])
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
