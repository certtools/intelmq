# SPDX-FileCopyrightText: 2023 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/spam_url.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Spam-URL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-spam_url-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'spam-url',
    'classification.taxonomy': 'abusive-content',
    'classification.type': 'spam',
    'extra.relay.asn': 64512,
    'extra.relay.geolocation.cc': 'ZZ',
    'extra.relay.geolocation.city': 'City',
    'extra.relay.geolocation.region': 'Region',
    'extra.relay.ip': '192.168.0.1',
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.subject': '104.145.232.222,abc,edf,587',
    'feed.name': 'Spam-URL',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.fqdn': 'node01.example.com',
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.url': 'https://192.168.0.1',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'spam-url',
    'classification.taxonomy': 'abusive-content',
    'classification.type': 'spam',
    'extra.relay.asn': 64512,
    'extra.relay.geolocation.cc': 'ZZ',
    'extra.relay.geolocation.city': 'City',
    'extra.relay.geolocation.region': 'Region',
    'extra.relay.ip': '192.168.0.2',
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.subject': '104.145.239.114,a,a,587',
    'feed.name': 'Spam-URL',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.fqdn': 'node02.example.com',
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.url': 'https://192.168.0.2',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'spam-url',
    'classification.taxonomy': 'abusive-content',
    'classification.type': 'spam',
    'extra.relay.asn': 64512,
    'extra.relay.geolocation.cc': 'ZZ',
    'extra.relay.geolocation.city': 'City',
    'extra.relay.geolocation.region': 'Region',
    'extra.relay.ip': '192.168.0.3',
    'feed.name': 'Spam-URL',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.fqdn': 'node03.example.com',
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.url': 'https://192.168.0.3/ggg/battle/?login=onthebend1@yahoo.com',
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
