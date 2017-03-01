# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.openbl.parser import OpenBLParserBot

with open(os.path.join(os.path.dirname(__file__), 'date_all.txt'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'blacklist',
           'raw': 'MTkyLjg4Ljk5LjQJMTQ3ODc5MDY4Mw==',
           'source.ip': '192.88.99.4',
           'time.source': '2016-11-10T15:11:23+00:00'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'blacklist',
           'raw': 'MTkyLjAuMC41CTE0Nzg3OTA1NTM=',
           'source.ip': '192.0.0.5',
           'time.source': '2016-11-10T15:09:13+00:00'}


class TestOpenBLParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Malc0deDomainBlacklistParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenBLParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
