# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.taichung.parser import TaichungCityNetflowParserBot

with open(os.path.join(os.path.dirname(__file__), 'recent30.html'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'malware',
           'event_description.text': 'Malware Provider',
           'raw': 'PHRkPjE8L3RkPjx0ZD48aW1nIHNyYz0icmVjZW50MzBfZmlsZXMvdXMuZ2lmIiBhbHQ9IiI+PHNwYW4'
                  'gc3R5bGU9ImNvbG9yOiBibGFjazsiPjE5Mi44OC45OS40PC9zcGFuPjwvdGQ+PHRkPk1hbHdhcmUgUH'
                  'JvdmlkZXI8L3RkPgogICAgICAgIDx0ZD7miYvli5XoqK3lrpo8L3RkPjx0ZD4yMDE2LTExLTA4IDIyO'
                  'jQ5OjE3PC90ZD48dGQ+Mi4wMjwvdGQ+CiAgICAgICAgPHRkIHN0eWxlPSJjb2xvcjpyZWQ7Ij7lsIHp'
                  'jpY8L3RkPjwvdHI+ICAgICAgICA=',
           'source.ip': '192.88.99.4',
           'time.source': '2016-11-08T14:49:17+00:00'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'malware',
           'event_description.text': 'Malware Provider',
           'raw': 'PHRkPjI8L3RkPjx0ZD48aW1nIHNyYz0icmVjZW50MzBfZmlsZXMvcnUuZ2lmIiBhbHQ9IiI+PHNwYW4'
                  'gc3R5bGU9ImNvbG9yOiBibGFjazsiPjE5Mi4wLjAuNTwvc3Bhbj48L3RkPjx0ZD5NYWx3YXJlIFByb3'
                  'ZpZGVyPC90ZD4KICAgICAgICA8dGQ+5omL5YuV6Kit5a6aPC90ZD48dGQ+MjAxNi0xMS0wOCAyMjo0N'
                  'jo0NDwvdGQ+PHRkPjIuMDI8L3RkPgogICAgICAgIDx0ZCBzdHlsZT0iY29sb3I6cmVkOyI+PC90ZD48'
                  'L3RyPiAgPC90Ym9keT4KICA8L3RhYmxlPgoKICA8aHI+CiAgPHRhYmxlIGNsYXNzPSJuZXRib3R0b21'
                  '0YmwiIGJvcmRlcj0iMCI+PHRib2R5Pg==',
           'source.ip': '192.0.0.5',
           'time.source': '2016-11-08T14:46:44+00:00'}


class TestTaichungCityNetflowParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TaichungCityNetflowParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TaichungCityNetflowParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
