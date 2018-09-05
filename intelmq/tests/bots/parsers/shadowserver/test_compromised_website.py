# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'compromised_website.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Compromised Website",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Compromised Website',
           'classification.taxonomy': 'intrusions',
           'classification.type': 'compromised',
           'classification.identifier': 'compromised-website',
           'extra.server': 'Microsoft-IIS/7.5',
           'extra.system': 'WINNT',
           'extra.detected_since': '2015-05-09 05:51:12',
           'protocol.application': 'http',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 64496,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '203.0.113.1',
           'source.port': 80,
           'source.url': 'http://example.com/header.php',
           'source.fqdn': 'example.com',
           'source.reverse_dns': 'example.com',
           'malware.name': 'hacked-webserver-stealrat-t1',
           'event_description.text': 'spam',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-01-16T00:43:48+00:00'},
          {'__type': 'Event',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'classification.identifier': 'compromised-website',
           'classification.taxonomy': 'intrusions',
           'classification.type': 'compromised',
           'event_description.text': 'phishing',
           'feed.name': 'ShadowServer Compromised Website',
           'malware.name': 'phishing',
           'protocol.application': 'http',
           'source.asn': 64496,
           'source.fqdn': 'example.com',
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'GRAZ',
           'source.geolocation.region': 'STEIERMARK',
           'source.ip': '203.0.113.1',
           'source.port': 80,
           'source.url': 'http://example.com/',
           'time.source': '2018-04-09T15:43:41+00:00'},
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Compromised-Website'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
