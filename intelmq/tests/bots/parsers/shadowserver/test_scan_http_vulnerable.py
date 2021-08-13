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
                       'testdata/scan_http_vulnerable.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Vulnerable HTTP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2021-08-01T09:00:00+00:00",
                  "extra.file_name": "2021-08-01-scan_http_vulnerable-test-test.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Vulnerable HTTP',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'classification.identifier': 'accessible-http',
           'extra.http': 'HTTP/1.1',
           'extra.http_code': 401,
           'extra.http_reason': 'Unauthorized',
           'extra.content_type': 'text/html; charset=%s',
           'extra.connection': 'close',
           'extra.server': 'mini_httpd/1.28 04Feb2018',
           'extra.http_date': '2000-11-25T20:21:50+00:00',
           'protocol.transport': 'tcp',
           'extra.tag': 'basic-auth,http',
           'extra.www_authenticate': 'Basic realm="Managed Switch"',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 1234,
           'source.geolocation.cc': 'EE',
           'source.geolocation.city': 'TARTU',
           'source.geolocation.region': 'TARTUMAA',
           'source.ip': '210.181.42.1',
           'source.port': 8000,
           'time.observation': '2021-08-01T09:00:00+00:00"',
           'time.source': '2021-08-01T07:00:24+00:00'},
          {'__type': 'Event',
           'feed.name': 'Vulnerable HTTP',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'classification.identifier': 'accessible-http',
           'extra.http': 'HTTP/1.1',
           'extra.http_code': 401,
           'extra.http_reason': 'Unauthorized',
           'extra.server': 'Web Server',
           'extra.content_type': 'text/html; charset=ISO-8859-1',
           'extra.connection': 'close',
           'extra.http_date': '2021-08-01T10:02:39+00:00',
           'extra.tag': 'basic-auth,http',
           'extra.www_authenticate': 'Basic realm="streaming_server"',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.reverse_dns': 'host.invalid',
           'source.asn': 5678,
           'source.geolocation.cc': 'EE',
           'source.geolocation.city': 'TALLINN',
           'source.geolocation.region': 'HARJUMAA',
           'source.ip': '22.23.35.23',
           'source.port': 8000,
           'time.observation': '2021-08-01T09:00:00+00:00"',
           'time.source': '2021-08-01T07:02:32+00:00'},
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
