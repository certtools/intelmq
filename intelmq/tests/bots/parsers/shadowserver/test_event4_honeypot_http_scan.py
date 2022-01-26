# SPDX-FileCopyrightText: 2021 Mikk Margus Möll <mikk@cert.ee>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_honeypot_http_scan.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Honeypot-HTTP-Scan',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2021-08-01T12:00:00+00:00",
                  "extra.file_name": "2021-08-01-event4_honeypot_http_scan.csv",
                  }

EVENTS = [{'__type': 'Event',
           'feed.name': 'Honeypot-HTTP-Scan',
           'classification.identifier': 'event-honeypot-http-scan',
           'classification.taxonomy': 'information-gathering',
           'classification.type': 'scanner',
           'destination.asn': 5678,
           'destination.geolocation.cc': 'UK',
           'destination.geolocation.city': 'MAIDENHEAD',
           'destination.geolocation.region': 'WINDSOR AND MAIDENHEAD',
           'destination.ip': '109.87.65.43',
           'destination.port': 80,
           'extra.http_url': '/js/ueditor/wwwroot/way-board.cgi',
           'extra.destination.naics': 518210,
           'protocol.transport': 'tcp',
           'extra.public_source': 'CAPRICA-EU',
           'extra.request_raw': 'GET /js/ueditor/wwwroot/way-board.cgi HTTP/1.0rnAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8rnAccept-Encoding: gzip, deflaternAccept-Language: en-US,en;q=0.5rnConnection: closernDnt: 1rnHost: 109.87.65.43rnOrigin: http://109.87.65.43rnReferer: http://109.87.65.43/rnUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3084.400 QQBrowser/9.6.11346.400',
           'extra.source.naics': 518210,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.version': '3.1.3-dev',
           'malware.name': 'http-scan',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 1234,
           'source.geolocation.cc': 'EE',
           'source.geolocation.city': 'TALLINN',
           'source.geolocation.region': 'HARJUMAA',
           'source.ip': '191.23.45.67',
           'source.port': 36455,
           'source.reverse_dns': '191-23-45-67-host.example.com',
           'time.observation': '2021-08-01T12:00:00+00:00',
           'time.source': '2021-08-01T00:24:08+00:00'},
          {'__type': 'Event',
           'feed.name': 'Honeypot-HTTP-Scan',
           'classification.identifier': 'event-honeypot-http-scan',
           'classification.taxonomy': 'information-gathering',
           'classification.type': 'scanner',
           'destination.asn': 23456,
           'destination.geolocation.cc': 'UA',
           'destination.geolocation.city': 'KHARKIV',
           'destination.geolocation.region': "KHARKIVS'KA OBLAST'",
           'destination.ip': '82.41.20.10',
           'destination.port': 8080,
           'extra.http_url': '/',
           'extra.http_request_method': 'GET',
           'protocol.transport': 'tcp',
           'extra.public_source': 'CAPRICA-EU',
           'extra.request_raw': 'R0VUIC8gSFRUUC8xLjENCkhvc3Q6IDgyLjQxLjIwLjEwOjgwODANCkFjY2VwdDogdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksKi8qO3E9MC44DQpBY2NlcHQtRW5jb2Rpbmc6IGRlZmxhdGUsIGd6aXAsIGlkZW50aXR5DQpBY2NlcHQtTGFuZ3VhZ2U6IGVuLVVTO3E9MC42LGVuO3E9MC40DQpVc2VyLUFnZW50OiBNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA1LjE7IHJ2OjkuMC4xKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzkuMC4xDQoNCg==',
           'extra.url_scheme': 'http',
           'extra.http_agent': 'Mozilla/5.0 (Windows NT 5.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
           'malware.name': 'http-scan',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 12345,
           'source.geolocation.cc': 'EE',
           'source.geolocation.city': 'TALLINN',
           'source.geolocation.region': 'HARJUMAA',
           'source.ip': '45.67.89.123',
           'source.port': 58610,
           'time.observation': '2021-08-01T12:00:00+00:00',
           'time.source': '2021-08-01T05:21:59+00:00'},
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
