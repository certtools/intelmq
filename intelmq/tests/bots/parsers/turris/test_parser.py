# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.turris.parser import TurrisGreylistParserBot

with open(os.path.join(os.path.dirname(__file__), 'greylist-latest.csv'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'scanner',
           'event_description.text': 'dns',
           'source.geolocation.cc': 'AU',
           'source.asn': 15169,
           'raw': 'MS4xLjEuMixBVSxkbnMsMTUxNjk=',
           'source.ip': '1.1.1.2'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'scanner',
           'event_description.text': 'telnet',
           'raw': 'MS4yMC45Ni4xNDIsVEgsdGVsbmV0LDU2MTIw',
           'source.geolocation.cc': 'TH',
           'source.asn': 56120,
           'source.ip': '1.20.96.142'}


class TestTurrisGreylistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TurrisGreylistParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TurrisGreylistParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
