# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.netlab_360.parser import Netlab360ParserBot

with open(os.path.join(os.path.dirname(__file__), 'dga.txt')) as handle:
    DGA_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'magnitude.txt')) as handle:
    MAGNITUDE_FILE = handle.read()

DGA_REPORT = {'feed.name': 'Netlab 360 DGA',
              'feed.url': 'http://data.netlab.360.com/feeds/dga/dga.txt',
              '__type': 'Report',
              'time.observation': '2016-01-01T00:00:00+00:00',
              'raw': utils.base64_encode(DGA_FILE),
             }

DGA_EVENTS = {'feed.name': 'Netlab 360 DGA',
              'feed.url': 'http://data.netlab.360.com/feeds/dga/dga.txt',
              '__type': 'Event',
              'time.observation': '2016-01-01T00:00:00+00:00',
              'time.source': '2016-11-13T00:04:15+00:00',
              'source.fqdn': 'difficultdress.net',
              'classification.type': 'c&c',
              'classification.identifier': 'suppobox',
              'event_description.url': 'http://data.netlab.360.com/dga',
              'raw': 'c3VwcG9ib3gJZGlmZmljdWx0ZHJlc3MubmV0CTIwMTYtMTEtMTIgMTE6NTg6NTYJMjAxNi0xMS0xMyAwMDowNDoxNQ==',
             }

MAGNITUDE_REPORT = {'feed.name': 'Netlab 360 Magnitude',
                    'feed.url': 'http://data.netlab.360.com/feeds/ek/magnitude.txt',
                    '__type': 'Report',
                    'time.observation': '2016-01-01T00:00:00+00:00',
                    'raw': utils.base64_encode(MAGNITUDE_FILE)
                   }

MAGNITUDE_EVENTS = {'feed.name': 'Netlab 360 Magnitude',
                    'feed.url': 'http://data.netlab.360.com/feeds/ek/magnitude.txt',
                    '__type': 'Event',
                    'time.observation': '2016-01-01T00:00:00+00:00',
                    'time.source': '2016-11-12T10:31:05+00:00',
                    'source.fqdn': '3ebo08o4ct0f6n2336.insides.party',
                    'source.ip': '178.32.227.12',
                    'source.url': 'http://3ebo08o4ct0f6n2336.insides.party/d97cc5cfab47e305536690a9987115ac',
                    'classification.type': 'exploit',
                    'classification.identifier': 'magnitude',
                    'event_description.url': 'http://data.netlab.360.com/ek',
                    'raw': 'TWFnbml0dWRlCTE0Nzg5NDY2NjUJMTc4LjMyLjIyNy4xMgkzZWJvMDhvNGN0MGY2bjIzMzYuaW5zaWRlcy5wYXJ0eQlodHRwOi8vM2VibzA4bzRjdDBmNm4yMzM2Lmluc2lkZXMucGFydHkvZDk3Y2M1Y2ZhYjQ3ZTMwNTUzNjY5MGE5OTg3MTE1YWM='
                   }


class TestNetlab360ParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for Netlab360ParserBot with DGA and Magnitude feeds. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Netlab360ParserBot
        cls.default_input_message = DGA_REPORT

    def test_DGA(self):
        self.run_bot()
        self.assertMessageEqual(0, DGA_EVENTS)

    def test_magnitude(self):
        self.input_message = MAGNITUDE_REPORT
        self.run_bot()
        self.assertMessageEqual(0, MAGNITUDE_EVENTS)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
