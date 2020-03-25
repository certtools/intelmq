# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.taichung.parser import TaichungNetflowRecentParserBot

with open(os.path.join(os.path.dirname(__file__), 'recent.html'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'brute-force',
           'event_description.text': 'Office 365 Attack',
           'raw': 'PHRkPjI8L3RkPjx0ZD48aW1nIHNyYz0iL2ltYWdlcy9mbGFncy9wbC5naWYiIGFsdD0iIj48c3BhbiBzdHlsZT0iY29sb3I6IGJsYWNrOyI+MTkyLjg4Ljk5LjQ8L3NwYW4+PC90ZD48dGQ+T2ZmaWNlIDM2NSBBdHRhY2s8L3RkPgogICAgICAgIDx0ZD7miYvli5XoqK3lrpo8L3RkPjx0ZD4yMDE5LTEwLTI5IDEzOjE4OjQ3PC90ZD48dGQ+MTQ3LjQ5PC90ZD4KICAgICAgICA8dGQgc3R5bGU9ImNvbG9yOnJlZDsiPuWwgemOljwvdGQ+PC90cj4gICAgICAgIA==',
           'source.ip': '192.88.99.4',
           'source.geolocation.cc': 'PL',
           'time.source': '2019-10-29T05:18:47+00:00'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'malware',
           'event_description.text': '惡意程式儲存FTP站',
           'raw': 'PHRkPjEyMzc8L3RkPjx0ZD48aW1nIHNyYz0iL2ltYWdlcy9mbGFncy9mci5naWYiIGFsdD0iIj48c3BhbiBzdHlsZT0iY29sb3I6IGJsYWNrOyI+MTkyLjAuMC41PC9zcGFuPjwvdGQ+PHRkPuaDoeaEj+eoi+W8j+WEsuWtmEZUUOermTwvdGQ+CiAgICAgICAgPHRkPuaJi+WLleioreWumjwvdGQ+PHRkPjIwMTMtMDQtMjQgMDA6MDE6NTk8L3RkPjx0ZD4yNTI3LjA0PC90ZD4KICAgICAgICA8dGQgc3R5bGU9ImNvbG9yOnJlZDsiPuWwgemOljwvdGQ+PC90cj4gICAgICAgIA==',
           'source.ip': '192.0.0.5',
           'source.geolocation.cc': 'FR',
           'time.source': '2013-04-23T16:01:59+00:00'}
OUTPUT3 = {'__type': 'Event',
           'classification.type': 'scanner',
           'event_description.text': 'SCAN-PORT-RDP',
           'raw': 'PHRkPjQ3NzQ8L3RkPjx0ZD48c3BhbiBzdHlsZT0iY29sb3I6IGJsYWNrOyI+PGEgaHJlZj0iaHR0cDovL3d3dy53aG9pczM2NS5jb20vdHcvaXAvMTAuMC4wLjEiIHRhcmdldD0iX2JsYW5rIj4xMC4wLjAuMTwvYT48L3NwYW4+PC90ZD48dGQ+U0NBTi1QT1JULVJEUDwvdGQ+CiAgICAgICAgPHRkPjkwNTwvdGQ+PHRkPjIwMjAtMDMtMjQgMDE6MTU6NTA8L3RkPjx0ZD4wLjk5PC90ZD4KICAgICAgICA8dGQgc3R5bGU9ImNvbG9yOnJlZDsiPuWwgemOljwvdGQ+PC90cj4gICAgICAgIA==',
           'source.ip': '10.0.0.1',
           'time.source': '2020-03-23T17:15:50+00:00'}
OUTPUT4 = {'__type': 'Event',
           'classification.type': 'scanner',
           'event_description.text': 'SCAN-PORT-137-138-139',
           'raw': 'PHRkPjQ4MDA8L3RkPjx0ZD48aW1nIHNyYz0iL2ltYWdlcy9mbGFncy91cy5naWYiIGFsdD0iIj48c3BhbiBzdHlsZT0iY29sb3I6IGJsYWNrOyI+PGEgaHJlZj0iaHR0cDovL3d3dy53aG9pczM2NS5jb20vdHcvaXAvMTI3LjAuMC4xIiB0YXJnZXQ9Il9ibGFuayI+MTI3LjAuMC4xPC9hPjwvc3Bhbj48L3RkPjx0ZD5TQ0FOLVBPUlQtMTM3LTEzOC0xMzk8L3RkPgogICAgICAgIDx0ZD43NjM8L3RkPjx0ZD4yMDIwLTAzLTI0IDAxOjE0OjI0PC90ZD48dGQ+MC45OTwvdGQ+CiAgICAgICAgPHRkIHN0eWxlPSJjb2xvcjpyZWQ7Ij7lsIHpjpY8L3RkPjwvdHI+ICA8L3Rib2R5PgogIDwvdGFibGU+CgogIDxocj4KICA8dGFibGUgYm9yZGVyPSIwIiBjbGFzcz0ibmV0Ym90dG9tdGJsIj4=',
           'source.ip': '127.0.0.1',
           'source.geolocation.cc': 'US',
           'time.source': '2020-03-23T17:14:24+00:00'}


class TestTaichungNetflowRecentParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TaichungNetflowRecentParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TaichungNetflowRecentParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)
        self.assertMessageEqual(2, OUTPUT3)
        self.assertMessageEqual(3, OUTPUT4)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
