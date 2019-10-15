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

with open(os.path.join(os.path.dirname(__file__), 'mirai.txt')) as handle:
    MIRAI_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'hajime.txt')) as handle:
    HAJIME_FILE = handle.read()


DGA_REPORT = {'feed.name': 'Netlab 360 DGA',
              'feed.url': 'http://data.netlab.360.com/feeds/dga/dga.txt',
              '__type': 'Report',
              'time.observation': '2018-01-01T00:00:00+00:00',
              'raw': utils.base64_encode(DGA_FILE),
             }

DGA_EVENT0 = {'feed.name': 'Netlab 360 DGA',
              'feed.url': 'http://data.netlab.360.com/feeds/dga/dga.txt',
              '__type': 'Event',
              'time.observation': '2018-01-01T00:00:00+00:00',
              #'time.source': '2016-11-13T00:04:15+00:00',
              'time.source': '2016-11-12T11:58:56+00:00',
              'source.fqdn': 'difficultdress.net',
              'classification.type': 'c2server',
              'classification.identifier': 'suppobox',
              'event_description.url': 'http://data.netlab.360.com/dga',
              'raw': 'c3VwcG9ib3gJZGlmZmljdWx0ZHJlc3MubmV0CTIwMTYtMTEtMTIgMTE6NTg6NTYJMjAxNi0xMS0xMyAwMDowNDoxNQ==',
             }
DGA_EVENT1 = {'feed.name': 'Netlab 360 DGA',
              'feed.url': 'http://data.netlab.360.com/feeds/dga/dga.txt',
              '__type': 'Event',
              'time.observation': '2018-01-01T00:00:00+00:00',
              'time.source': '2018-01-01T00:00:00+00:00',
              'source.fqdn': 'example.com',
              'classification.type': 'c2server',
              'classification.identifier': 'foobar',
              'event_description.url': 'http://data.netlab.360.com/dga',
              'raw': 'Zm9vYmFyCWV4YW1wbGUuY29tCTIwMTgtMDEtMDEgMDA6MDA6MDAJMjAzMC0wNS0wNCAwMDowODowOA==',
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

MIRAI_REPORT = {'feed.name': 'Netlab 360 Mirai Scanner',
                    'feed.url': 'http://data.netlab.360.com/feeds/mirai-scanner/scanner.list',
                    '__type': 'Report',
                    'time.observation': '2016-01-01T00:00:00+00:00',
                    'raw': utils.base64_encode(MIRAI_FILE)
                   }

MIRAI_EVENTS = {'feed.name': 'Netlab 360 Mirai Scanner',
                    'feed.url': 'http://data.netlab.360.com/feeds/mirai-scanner/scanner.list',
                    '__type': 'Event',
                    'destination.port': 23,
                    'time.observation': '2016-01-01T00:00:00+00:00',
                    'time.source': '2016-08-01T12:46:01+00:00',
                    'source.ip': '109.86.182.249',
                    'classification.type': 'scanner',
                    'classification.identifier': 'mirai',
                    'raw': 'MjAxNi0wOC0wMSAxMjo0NjowMQlzaXA9MTA5Ljg2LjE4Mi4yNDkJZHBvcnQ9MjM=',
                   }
HAJIME_REPORT = {'feed.name': 'Netlab 360 Hajime Scanner',
                 'feed.url': 'https://data.netlab.360.com/feeds/hajime-scanner/bot.list',
                 '__type': 'Report',
                 'time.observation': '2016-01-01T00:00:00+00:00',
                 'raw': utils.base64_encode(HAJIME_FILE)
                 }

HAJIME_EVENTS = {'feed.name': 'Netlab 360 Hajime Scanner',
                 'feed.url': 'https://data.netlab.360.com/feeds/hajime-scanner/bot.list',
                 '__type': 'Event',
                 'time.observation': '2016-01-01T00:00:00+00:00',
                 'time.source': '2017-09-11T00:00:00+00:00',
                 'source.ip': '192.0.2.45',
                 'classification.type': 'scanner',
                 'classification.identifier': 'hajime',
                 'raw': 'MjAxNy0wOS0xMQlpcD0xOTIuMC4yLjQ1',
                   }


class TestNetlab360ParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for Netlab360ParserBot with DGA and Magnitude feeds. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Netlab360ParserBot
        cls.default_input_message = DGA_REPORT

    def test_DGA(self):
        self.run_bot()
        self.assertMessageEqual(0, DGA_EVENT0)
        # the time is in the future here
        self.assertMessageEqual(1, DGA_EVENT1)

    def test_magnitude(self):
        self.input_message = MAGNITUDE_REPORT
        self.run_bot()
        self.assertMessageEqual(0, MAGNITUDE_EVENTS)

    def test_mirai(self):
        self.input_message = MIRAI_REPORT
        self.run_bot()
        self.assertMessageEqual(0, MIRAI_EVENTS)

    def test_hajime(self):
        self.input_message = HAJIME_REPORT
        self.run_bot()
        self.assertMessageEqual(0, HAJIME_EVENTS)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
