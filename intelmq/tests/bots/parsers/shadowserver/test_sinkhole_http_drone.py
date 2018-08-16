# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'Sinkhole-HTTP-Drone.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Sinkhole HTTP Drone",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Sinkhole HTTP Drone',
           'classification.taxonomy': 'malicious code',
           'classification.type': 'infected system',
           'destination.asn': 6939,
           'destination.geolocation.cc': 'US',
           'destination.fqdn': '198-51-100-55.example.net',
           'destination.ip': '198.51.100.248',
           'destination.port': 80,
           'malware.name': 'avalanche-goznym',
           'protocol.transport': 'tcp',
           'protocol.application': 'http',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 34502,
           'source.geolocation.cc': 'AT',
           'source.ip': '198.51.100.55',
           'source.port': 63339,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2018-03-05T00:00:01+00:00',
           },
          {'__type': 'Event',
           'feed.name': 'ShadowServer Sinkhole HTTP Drone',
           'classification.taxonomy': 'malicious code',
           'classification.type': 'infected system',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.geolocation.cc': 'AT',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'destination.asn': 393667,
           'destination.geolocation.cc': 'US',
           'destination.ip': '198.51.100.22',
           'destination.port': 80,
           'destination.url': 'http://198.51.100.90/search?q=1',
           'extra.user_agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; '
                               'SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR '
                               '3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
           'malware.name': 'downadup',
           'protocol.transport': 'tcp',
           'protocol.application': 'http',
           'source.asn': 8447,
           'source.ip': '198.51.100.155',
           'source.port': 4457,
           'time.source': '2018-03-05T00:00:06+00:00',
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
        cls.sysconfig = {'feedname': 'Sinkhole-HTTP-Drone'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
