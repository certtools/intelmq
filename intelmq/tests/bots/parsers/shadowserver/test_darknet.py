# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/darknet.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Darknet",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-darknet-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'mirai-like',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.port': 8001,
           'extra.count': 1,
           'extra.naics': 518210,
           'extra.public_source': 'sissden',
           'extra.sic': 737415,
           'feed.name': 'ShadowServer Darknet',
           'source.asn': 64496,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '198.51.100.47',
           'source.reverse_dns': '198-51-100-47.example.net',
           'time.source': '2018-11-19T00:00:17+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'mirai-like',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.port': 80,
           'extra.count': 2,
           'extra.public_source': 'sissden',
           'feed.name': 'ShadowServer Darknet',
           'source.asn': 64497,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'DEUTSCHLANDSBERG',
           'source.geolocation.region': 'STEIERMARK',
           'source.ip': '198.51.100.4',
           'source.reverse_dns': '198-51-100-4.example.net',
           'time.source': '2018-11-19T00:00:25+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'mirai-like',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.port': 5555,
           'extra.count': 2,
           'extra.naics': 518210,
           'extra.public_source': 'sissden',
           'extra.sector': 'Information Technology',
           'extra.sic': 737401,
           'feed.name': 'ShadowServer Darknet',
           'source.asn': 64498,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '198.51.100.146',
           'time.source': '2018-11-19T22:58:23+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
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

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
