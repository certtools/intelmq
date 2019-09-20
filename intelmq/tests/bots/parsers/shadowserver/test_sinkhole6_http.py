# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/sinkhole6_http.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer IPv6 Sinkhole HTTP Drone",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-sinkhole6_http-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.taxonomy': 'malicious code',
           'classification.type': 'infected-system',
           'destination.asn': 64511,
           'destination.fqdn': '198-51-100-38.example.net',
           'destination.geolocation.cc': 'NL',
           'destination.ip': '2a02:1668:1034::2',
           'destination.port': 80,
           'destination.url': 'http://198-51-100-38.example.net/okla/api/1',
           'feed.name': 'ShadowServer IPv6 Sinkhole HTTP Drone',
           'malware.name': 'ghost-push',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 64511,
   'source.geolocation.cc': 'AT',
           'source.ip': '2001:db8:abcd:12::',
           'source.port': 36738,
           'time.source': '2018-04-08T09:17:36+00:00'},
          {'__type': 'Event',
           'classification.taxonomy': 'malicious code',
           'classification.type': 'infected-system',
           'destination.asn': 64511,
           'destination.fqdn': '198-51-100-38.example.net',
           'destination.geolocation.cc': 'NL',
           'destination.ip': '2a02:1668:1034::2',
           'destination.port': 80,
           'extra.http_agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
                               'Gecko/20100101 Firefox/40.1',
           'destination.url': 'http://198-51-100-38.example.net/',
           'feed.name': 'ShadowServer IPv6 Sinkhole HTTP Drone',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 64511,
           'source.geolocation.cc': 'AT',
           'source.ip': '2001:db8:abcd:12::',
           'source.port': 33306,
           'time.source': '2018-04-08T15:03:03+00:00'},
          {'__type': 'Event',
           'classification.taxonomy': 'malicious code',
           'classification.type': 'infected-system',
           'destination.asn': 64511,
           'destination.fqdn': '198-51-100-38.example.net',
           'destination.geolocation.cc': 'NL',
           'destination.ip': '2a02:1668:1034::2',
           'destination.port': 80,
           'extra.http_agent': 'Mercury/907 CFNetwork/758.5.3 Darwin/15.6.0',
           'destination.url': 'http://198-51-100-38.example.net/',
           'feed.name': 'ShadowServer IPv6 Sinkhole HTTP Drone',
           'malware.name': 'xcodeghost',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           'source.asn': 64511,
           'source.geolocation.cc': 'AT',
           'source.ip': '2001:db8:abcd:12::',
           'source.port': 52394,
           'time.source': '2018-04-08T19:57:45+00:00'},
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
