# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'compromised_website.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

with open(os.path.join(os.path.dirname(__file__),
                       'compromised_website_RECONSTRUCTED.csv')) as handle:
    RECONSTRUCTED_FILE = handle.read()
RECONSTRUCTED_LINES = RECONSTRUCTED_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Compromised Website",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENT = {'__type': 'Event',
         'feed.name': 'ShadowServer Compromised Website',
         'classification.type': 'compromised',
         'classification.identifier': 'compromised-website',
         'extra': '{"detected_since": "2015-05-09 05:51:12", "naics": "0", "server": '
                  '"Microsoft-IIS/7.5", "sic": "0", "system": "WINNT"}',
         'protocol.application': 'http',
         'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                               RECONSTRUCTED_LINES[1], ''])),
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
       'time.source': '2017-01-16T00:43:48+00:00'}


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
        self.assertMessageEqual(0, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
