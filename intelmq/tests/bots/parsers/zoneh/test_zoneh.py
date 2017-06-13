# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.zoneh.parser import ZoneHParserBot

with open(
    os.path.join(os.path.dirname(__file__), 'defacement_accepted.csv')
) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()


EXAMPLE_REPORT = {"feed.name": "ZoneH Defacements",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENT00 = {
    '__type': 'Event',
    'feed.name': 'ZoneH Defacements',
    'classification.type': 'compromised',
    'classification.identifier': 'compromised-website',
    'extra': '{"accepted_date": "2016-06-01 13:20:21" }',
    'protocol.application': 'http',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                          EXAMPLE_LINES[1], ''])),
    'source.asn': 64496,
    'source.geolocation.cc': 'ZZ',
    'source.ip': '203.0.113.1',
    'source.port': 80,
    'source.url': 'http://defaced.example.com',
    'source.fqdn': 'defaced.example.com',
    'event_description.text': 'defacement',
    'time.observation': '2015-01-01T00:00:00+00:00',
    'time.source': '2017-01-16T00:43:48+00:00'}


class TestZoneHParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ZoneHParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ZoneHParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Compromised-Website'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENT00)
        #self.assertMessageEqual(1, EVENT01)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
