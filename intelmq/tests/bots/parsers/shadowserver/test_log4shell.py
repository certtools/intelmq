# SPDX-FileCopyrightText: 2022 CERT.at GmbH <waldbauer@cert.at>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_log4shell_vulnerable.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Vulnerable Log4J',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2021-12-13T09:00:00+00:00",
                  "extra.file_name": "2021-12-13-scan_log4shell_vulnerable-test-test.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Vulnerable Log4J',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable-system',
           'classification.identifier': 'log4shell',
           'extra.geo': 'IR',
           'extra.method': 'dns',
           'extra.public_source': 'alphastrike.io',
           'extra.status': 'vulnerable',
           'extra.tag': 'cve-2021-44228',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.ip': '198.51.100.147',
           'source.asn': 41881,
           'source.geolocation.city': 'TEHRAN',
           'source.geolocation.region': 'TEHRAN',
           'source.port': 80,
           'time.observation': '2021-12-13T13:58:00+00:00',
           'time.source': '2021-12-13T13:58:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'Vulnerable Log4J',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable-system',
           'classification.identifier': 'log4shell',
           'extra.naics': 454110,
           'extra.geo': 'US',
           'extra.method': 'dns',
           'extra.public_source': 'alphastrike.io',
           'extra.status': 'vulnerable',
           'extra.tag': 'cve-2021-44228',
           'protocol.transport': 'tcp',
           'extra.sector': 'Retail Trade',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.ip': '198.51.100.147',
           'source.asn': 14618,
           'source.geolocation.city': 'ASHBURN',
           'source.geolocation.region': 'VIRGINIA',
           'source.port': 443,
           'source.reverse_dns': '198-51-100-147.example.net',
           'time.observation': '2021-12-13T13:58:00+00:00',
           'time.source': '2021-12-13T13:58:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'Vulnerable Log4J',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable-system',
           'classification.identifier': 'log4shell',
           'extra.naics': 454110,
           'extra.geo': 'US',
           'extra.method': 'dns',
           'extra.public_source': 'alphastrike.io',
           'extra.status': 'vulnerable',
           'extra.tag': 'cve-2021-44228',
           'protocol.transport': 'tcp',
           'extra.sector': 'Retail Trade',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           'source.ip': '198.51.100.147',
           'source.asn': 14618,
           'source.geolocation.city': 'ASHBURN',
           'source.geolocation.region': 'VIRGINIA',
           'source.port': 8080,
           'source.reverse_dns': '198-51-100-147.example.net',
           'time.observation': '2021-12-13T13:58:00+00:00',
           'time.source': '2021-12-13T13:58:00+00:00'}
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
