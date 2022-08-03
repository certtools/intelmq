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
                       'testdata/sandbox_url.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Sandbox URL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-sandbox_url-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-url',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'malware-distribution',
   'destination.fqdn' : 'www.msftncsi.com',
   'extra.http_request_method' : 'GET',
   'destination.url' : 'http://www.msftncsi.com/ncsi.txt',
   'extra.user_agent' : 'Microsoft NCSI',
   'feed.name' : 'Sandbox URL',
   'malware.hash.md5' : '37514b54e679a5313334e830ad780ec7',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 20940,
   'source.geolocation.cc' : 'US',
   'source.ip' : '23.196.47.89',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:13+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-url',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'malware-distribution',
   'destination.fqdn' : 'www.download.windowsupdate.com',
   'extra.http_request_method' : 'GET',
   'destination.url' : 'http://www.download.windowsupdate.com/msdownload/update/v3/static/trustedr/en/authrootstl.cab',
   'extra.user_agent' : 'Microsoft-CryptoAPI/6.1',
   'feed.name' : 'Sandbox URL',
   'malware.hash.md5' : '37514b54e679a5313334e830ad780ec7',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 15133,
   'source.geolocation.cc' : 'US',
   'source.ip' : '72.21.81.240',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:28+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sandbox-url',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'malware-distribution',
   'destination.fqdn' : 'crl.microsoft.com',
   'extra.http_request_method' : 'GET',
   'destination.url' : 'http://crl.microsoft.com/pki/crl/products/MicTimStaPCA_2010-07-01.crl',
   'extra.user_agent' : 'Microsoft-CryptoAPI/6.1',
   'feed.name' : 'Sandbox URL',
   'malware.hash.md5' : 'e97ea2820c0d79f3f3ca241d4dcd1060',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 20940,
   'source.geolocation.cc' : 'US',
   'source.ip' : '23.56.4.57',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:08:24+00:00'
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
