# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import unittest
from intelmq.lib import utils
import intelmq.lib.test as test
from intelmq.bots.parsers.sucuri.parser import SucuriParserBot


with open(os.path.join(os.path.dirname(__file__), 'test_sucuri.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"feed.name": "Sucuri Hidden Iframes", "raw": utils.base64_encode(REPORT_DATA), "__type": "Report", "feed.url": "http://labs.sucuri.net/?malware", "time.observation": "2018-01-22T14:38:24+00:00", "feed.accuracy": 100.0}
EVENT1 = {"feed.accuracy": 100.0, "feed.url": "http://labs.sucuri.net/?malware", "__type": "Event", "classification.type": "blacklist", "source.url": "http://poseyhumane.org/stats.php", "raw": "PHRhYmxlIGNsYXNzPSJncHRhYmxlIG13dGFibGUgdGFibGUiPjx0aGVhZD48dHI+PHRoPiMgb2Ygc2l0ZXMgaW5mZWN0ZWQ8L3RoPjx0aD5UeXBlPC90aD48dGg+TWFsd2FyZSAvIERvbWFpbnM8L3RoPjwvdHI+PC90aGVhZD48dGJvZHk+PHRyPjx0ZD41NTwvdGQ+PHRkPjxhIGhyZWY9Ii8/dHlwZT1pZnJhbWUiPmlmcmFtZTwvYT48L3RkPjx0ZD48c3Bhbj48YSBocmVmPSIvP2RldGFpbHM9cG9zZXlodW1hbmUub3JnIj5odHRwOi8vcG9zZXlodW1hbmUmIzQ2O29yZy9zdGF0cyYjNDY7cGhwPC9hPjwvc3Bhbj48L3RkPjwvdHI+", "time.observation": "2018-01-24T14:23:34+00:00", "feed.name": "Sucuri Hidden Iframes", "classification.identifier": "hidden iframe"}
EVENT2 = {"classification.identifier": "hidden iframe", "feed.accuracy": 100.0, "time.observation": "2018-01-24T15:58:48+00:00", "__type": "Event", "feed.name": "Sucuri Hidden Iframes", "source.url": "http://zumobtr.ru/gate.php?f=1041671", "raw": "PHRyPjx0ZD42PC90ZD48dGQ+PGEgaHJlZj0iLz90eXBlPWlmcmFtZSI+aWZyYW1lPC9hPjwvdGQ+PHRkPjxzcGFuPjxhIGhyZWY9Ii8/ZGV0YWlscz16dW1vYnRyLnJ1Ij5odHRwOi8venVtb2J0ciYjNDY7cnUvZ2F0ZSYjNDY7cGhwP2Y9MTA0MTY3MTwvYT48L3NwYW4+PC90ZD48L3RyPg==", "feed.url": "http://labs.sucuri.net/?malware", "classification.type": "blacklist"}
EVENT3 = {"classification.identifier": "hidden iframe", "feed.accuracy": 100.0, "time.observation": "2018-01-24T15:58:48+00:00", "__type": "Event", "feed.name": "Sucuri Hidden Iframes", "source.url": "http://ads.rzb.ir/image.php?size_id=7", "raw": "PHRyPjx0ZD42PC90ZD48dGQ+PGEgaHJlZj0iLz90eXBlPWlmcmFtZSI+aWZyYW1lPC9hPjwvdGQ+PHRkPjxzcGFuPjxhIGhyZWY9Ii8/ZGV0YWlscz1hZHMucnpiLmlyIj5odHRwOi8vYWRzJiM0NjtyemImIzQ2O2lyL2ltYWdlJiM0NjtwaHA/c2l6ZV9pZD03PC9hPjwvc3Bhbj48L3RkPjwvdHI+", "feed.url": "http://labs.sucuri.net/?malware", "classification.type": "blacklist"}


class TestSucuriParserBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = SucuriParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':
    unittest.main()
