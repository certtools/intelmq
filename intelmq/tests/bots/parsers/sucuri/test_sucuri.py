# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import unittest
import intelmq.lib.test as test
from intelmq.bots.parsers.sucuri.parser import SucuriParserBot


with open(os.path.join(os.path.dirname(__file__), 'test_sucuri.data')) as handle:
    REPORT_DATA = handle.read().strip()

REPORT = {"feed.name": "Sucuri security", "raw": REPORT_DATA, "__type": "Report", "feed.url": "http://labs.sucuri.net/?malware", "time.observation": "2018-01-22T14:38:24+00:00", "feed.accuracy": 100.0}
EVENT = {'raw': 'PHRhYmxlIGNsYXNzPSJncHRhYmxlIG13dGFibGUgdGFibGUiPjx0aGVhZD48dHI+PHRoPiMgb2Ygc2l0ZXMgaW5mZWN0ZWQ8L3RoPjx0aD5UeXBlPC90aD48dGg+TWFsd2FyZSAvIERvbWFpbnM8L3RoPjwvdHI+PC90aGVhZD48dGJvZHk+PHRyPjx0ZD41NTwvdGQ+PHRkPjxhIGhyZWY9Ii8/dHlwZT1pZnJhbWUiPmlmcmFtZTwvYT48L3RkPjx0ZD48c3Bhbj48YSBocmVmPSIvP2RldGFpbHM9cG9zZXlodW1hbmUub3JnIj5odHRwOi8vcG9zZXlodW1hbmUmIzQ2O29yZy9zdGF0cyYjNDY7cGhwPC9hPjwvc3Bhbj48L3RkPjwvdHI+', 'classification.type': 'blacklist', "feed.name": "Sucuri security", "feed.accuracy": 100.0, "__type": "Event", "feed.url": "http://labs.sucuri.net/?malware", "time.observation": "2018-01-22T14:38:24+00:00", "source.url": "http://poseyhumane&#46;org/stats&#46;php"}


class TestSucuriParserBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = SucuriParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT)

if __name__ == '__main__':
    unittest.main()
