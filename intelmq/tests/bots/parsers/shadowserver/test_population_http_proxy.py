# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/population_http_proxy.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible HTTP Proxy',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-population_http_proxy-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'accessible-http-proxy',
    'classification.taxonomy': 'other',
    'classification.type': 'other',
    'extra.connection': 'keep-alive',
    'extra.content_length': 3741,
    'extra.content_type': 'text/html;charset=utf-8',
    'extra.http': 'HTTP/1.1',
    'extra.http_code': 407,
    'extra.http_date': '2010-02-10T00:00:00+00:00',
    'extra.http_reason': 'Proxy Authentication Required',
    'extra.proxy_authenticate': 'Basic realm=\\\\"Squid proxy-caching web '
                                'server\\"\\""',
    'extra.server': 'squid/4.10',
    'feed.name': 'Accessible HTTP Proxy',
    'malware.name': 'http-connect-proxy-closed',
    'protocol.application': 'http',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 3128,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-http-proxy',
    'classification.taxonomy': 'other',
    'classification.type': 'other',
    'extra.connection': 'keep-alive',
    'extra.content_length': 3833,
    'extra.content_type': 'text/html;charset=utf-8',
    'extra.http': 'HTTP/1.1',
    'extra.http_code': 407,
    'extra.http_date': '2010-02-10T00:00:01+00:00',
    'extra.http_reason': 'Proxy Authentication Required',
    'extra.proxy_authenticate': 'Basic realm=\\\\"00:23:24:43:1c:34\\"\\""',
    'feed.name': 'Accessible HTTP Proxy',
    'malware.name': 'http-connect-proxy-closed',
    'protocol.application': 'http',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 3128,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-http-proxy',
    'classification.taxonomy': 'other',
    'classification.type': 'other',
    'extra.connection': 'keep-alive',
    'extra.content_length': 179,
    'extra.content_type': 'text/html;charset=utf-8',
    'extra.http': 'HTTP/1.1',
    'extra.http_code': 407,
    'extra.http_date': '2010-02-10T00:00:02+00:00',
    'extra.http_reason': 'Proxy Authentication Required',
    'extra.proxy_authenticate': 'Basic realm=\\\\"Proxy\\"\\""',
    'feed.name': 'Accessible HTTP Proxy',
    'malware.name': 'http-connect-proxy-closed',
    'protocol.application': 'http',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 3128,
    'source.reverse_dns': 'node03.example.com',
    'time.source': '2010-02-10T00:00:02+00:00'
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
