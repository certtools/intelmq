# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/netis_router.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-netis_router-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'open-netis',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.response': 'Login:',
           'extra.sector': 'Information Technology',
           'extra.tag': 'netis_vulnerability',
           'feed.name': 'Open-Netis',
           'protocol.transport': 'udp',
           'source.asn': 64511,
           'source.geolocation.cc': 'DE',
           'source.geolocation.city': 'BERLIN',
           'source.geolocation.region': 'BERLIN',
           'source.ip': '198.51.100.77',
           'source.port': 53413,
           'time.source': '2019-08-04T01:36:49+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
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
