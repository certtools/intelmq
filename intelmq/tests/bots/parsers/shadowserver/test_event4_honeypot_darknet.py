# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_honeypot_darknet.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Darknet",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_honeypot_darknet.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'mirai',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.port': 23,
           'extra.source.naics': 518210,
           'extra.protocol': 'tcp',
           'feed.name': 'ShadowServer Darknet',
           'malware.name': 'mirai',
           'source.asn': 9829,
           'source.geolocation.cc': 'IN',
           'source.geolocation.city': 'CHENGANNUR',
           'source.geolocation.region': 'KERALA',
           'source.ip': '61.3.1.2',
           'source.port': 4717,
           'time.source': '2021-03-07T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'mirai',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.port': 23,
           'extra.protocol': 'tcp',
           'extra.source.naics': 517311,
           'feed.name': 'ShadowServer Darknet',
           'malware.name': 'mirai',
           'source.asn': 4766,
           'source.geolocation.cc': 'KR',
           'source.geolocation.city': 'PYEONGCHANG-EUP',
           'source.geolocation.region': 'GANGWON-DO',
           'source.ip': '211.218.3.4',
           'source.port': 4405,
           'time.source': '2021-03-07T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'mirai',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.port': 23,
           'extra.protocol': 'tcp',
           'feed.name': 'ShadowServer Darknet',
           'malware.name': 'mirai',
           'source.asn': 266915,
           'source.geolocation.cc': 'BR',
           'source.geolocation.city': 'VITORIA DA CONQUISTA',
           'source.geolocation.region': 'BAHIA',
           'source.ip': '45.225.5.6',
           'source.port': 59777,
           'source.reverse_dns': 'static-45-225-x-x.example.net',
           'time.source': '2021-03-07T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           },
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
