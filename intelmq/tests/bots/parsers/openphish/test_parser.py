# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.openphish.parser import OpenPhishParserBot

with open(os.path.join(os.path.dirname(__file__), 'feed.txt'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'phishing',
           'raw': 'aHR0cDovL3d3dy4uZXhhbXBsZS5jb20vcGhpc2hpbmc=',
           'source.url': 'http://www..example.com/phishing'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'phishing',
           'raw': 'aHR0cDovL3d3dy4uZXhhbXBsZS5pbnZhbGlkL3BoaXNoaW5n',
           'source.url': 'http://www..example.invalid/phishing'}


class TestOpenPhishParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for OpenPhishParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenPhishParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
