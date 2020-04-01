# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_dns.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2018-07-30T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_dns-test-test.csv",
                  'feed.name': 'report feedname',
                  }
EVENTS = [{
    '__type': 'Event',
    'feed.name': 'report feedname',
    "classification.identifier": "dns-open-resolver",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.dns_version": "dnsmasq-2.66",
    "extra.min_amplification": 4.619,
    "extra.tag": "openresolver",
    "protocol.application": "dns",
    "protocol.transport": "udp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                         EXAMPLE_LINES[1]])),
    "source.asn": 25255,
    "source.geolocation.cc": "AT",
    "source.geolocation.city": "VIENNA",
    "source.geolocation.region": "WIEN",
    "source.ip": "198.51.100.179",
    "source.port": 53,
    "source.reverse_dns": "198-51-100-189.example.net",
    "time.observation": "2018-07-30T00:00:00+00:00",
    "time.source": "2018-04-14T00:14:34+00:00"
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

    def test_default(self):
        """ Test if feed name is not overwritten has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)

    def test_overwrite_feed_name(self):
        """ Test if feed name is overwritten if asked to do so. """
        self.prepare_bot(parameters={'overwrite': True})
        self.run_bot(prepare=False)
        for i, EVENT in enumerate(EVENTS):
            event = EVENT.copy()
            event['feed.name'] = 'DNS-Open-Resolvers'
            self.assertMessageEqual(i, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
