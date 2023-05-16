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
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'accessible-http',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.content_length': 149,
    'extra.content_type': 'text/html; charset=utf-8',
    'extra.http': 'HTTP/1.1',
    'extra.http_code': 401,
    'extra.http_date': '2010-02-10T00:00:00+00:00',
    'extra.http_reason': 'Unauthorized',
    'extra.server': 'TwistedWeb/19.7.0',
    'extra.set_cookie': 'TWISTED_SESSION=5473ad3faa3de66685fb3a53bffb390b4fcec2039893009a06caf38e1bec8aa8',
    'extra.tag': 'basic-auth,http',
    'extra.www_authenticate': 'Basic realm=\\\\"OpenWebif\\"\\""',
    'feed.name': 'Vulnerable HTTP',
    'protocol.application': 'http',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 8080,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-http',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.content_length': 149,
    'extra.content_type': 'text/html; charset=utf-8',
    'extra.http': 'HTTP/1.1',
    'extra.http_code': 401,
    'extra.http_date': '2010-02-10T00:00:01+00:00',
    'extra.http_reason': 'Unauthorized',
    'extra.server': 'TwistedWeb/19.7.0',
    'extra.set_cookie': 'TWISTED_SESSION=d2460d37b7fdbdd6c27dd74423ead5704e553d4f2c230672313edc5602059e33',
    'extra.tag': 'basic-auth,http',
    'extra.www_authenticate': 'Basic realm=\\\\"OpenWebif\\"\\""',
    'feed.name': 'Vulnerable HTTP',
    'protocol.application': 'http',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 80,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-http',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.detail': 'repositoryformatversion = 0;filemode = false;bare = '
                    'false;logallrefupdates = true;symlinks = false;ignorecase = '
                    'true',
    'extra.http_date': '2010-02-10T00:00:02+00:00',
    'extra.tag': 'git-config-file',
    'feed.name': 'Vulnerable HTTP',
    'protocol.application': 'http',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 443,
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
