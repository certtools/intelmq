# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_tftp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open TFTP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-03-25T00:00:00+00:00",
                  "extra.file_name": "2019-03-25-scan_tftp-test-test.csv",
                  }
EVENTS = [{
            '__type': 'Event',
            'feed.name': 'Open TFTP',
            "classification.identifier": "scan-tftp",
            "classification.taxonomy": "vulnerable",
            "classification.type": "vulnerable-system",
            "extra.error": "Illegal TFTP operation",
            "extra.errorcode": "4",
            "extra.errormessage": "Illegal TFTP operation",
            "extra.source.naics": 517310,
            "extra.opcode": "5",
            "extra.source.sic": 481302,
            "extra.size": 27,
            "extra.tag": "tftp",
            "protocol.application": "tftp",
            "protocol.transport": "udp",
            'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
            "source.asn": 12843,
            "source.geolocation.cc": "DE",
            "source.geolocation.city": "KARLSRUHE",
            "source.geolocation.region": "BADEN-WURTTEMBERG",
            "source.ip": "198.51.100.152",
            "source.port": 69,
            "time.observation": "2019-03-25T00:00:00+00:00",
            "time.source": "2016-07-24T00:12:08+00:00"
          },
          {
            '__type': 'Event',
            'feed.name': 'Open TFTP',
            "classification.identifier": "scan-tftp",
            "classification.taxonomy": "vulnerable",
            "classification.type": "vulnerable-system",
            "extra.error": "Illegal TFTP operation",
            "extra.errorcode": "4",
            "extra.errormessage": "Illegal TFTP operation",
            "extra.source.naics": 541690,
            "extra.opcode": "5",
            "extra.source.sic": 874899,
            "extra.size": 27,
            "extra.tag": "tftp",
            "protocol.application": "tftp",
            "protocol.transport": "udp",
            'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
            "source.asn": 3320,
            "source.geolocation.cc": "DE",
            "source.geolocation.city": "DUSSELDORF",
            "source.geolocation.region": "NORDRHEIN-WESTFALEN",
            "source.ip": "198.51.100.67",
            "source.port": 11230,
            "time.observation": "2019-03-25T00:00:00+00:00",
            "time.source": "2016-07-24T00:12:08+00:00"
           }
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
