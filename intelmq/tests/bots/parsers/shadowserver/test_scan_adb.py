# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_adb.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible ADB',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2018-07-30T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_adb-test-test.csv",

                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible ADB',
           'time.observation': '2018-07-30T00:00:00+00:00',
           'time.source': '2018-07-26T02:07:16+00:00',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'accessible-adb',
           'protocol.application': 'adb',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 3462,
           'source.geolocation.cc': 'TW',
           'source.geolocation.city': 'TAOYUAN CITY',
           'source.geolocation.region': 'TAOYUAN COUNTY',
           'source.ip': '36.239.124.210',
           'source.port': 5555,
           'extra.name': 'hlteuc',
           'extra.model': 'SAMSUNG-SM-N900A',
           'extra.device': 'hlteatt',
           'extra.naics': 518210,
           'extra.sic': 737415,
           'extra.tag': 'adb',
           'source.reverse_dns': '36-239-124-210.dynamic-ip.hinet.net',
           },
          {'__type': 'Event',
           'feed.name': 'Accessible ADB',
           'time.observation': '2018-07-30T00:00:00+00:00',
           'time.source': '2018-07-26T02:07:16+00:00',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'accessible-adb',
           'protocol.application': 'adb',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 3462,
           'source.geolocation.cc': 'TW',
           'source.geolocation.city': 'TAIPEI',
           'source.geolocation.region': 'TAIPEI CITY',
           'source.ip': '36.236.108.107',
           'source.port': 5555,
           'extra.name': 'marlin',
           'extra.model': 'Pixel XL',
           'extra.device': 'marlin',
           'extra.features': 'cmd,shell_v2',
           'extra.naics': 518210,
           'extra.sic': 737415,
           'extra.tag': 'adb',
           'source.reverse_dns': '36-236-108-107.dynamic-ip.hinet.net',
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
