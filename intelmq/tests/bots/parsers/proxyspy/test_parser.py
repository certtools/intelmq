# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.proxyspy.parser import ProxyspyParserBot

with open(os.path.join(os.path.dirname(__file__), 'proxy.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {'feed.name': 'Proxy Spy',
                  'feed.url': 'http://txt.proxyspy.net/proxy.txt',
                  '__type': 'Report',
                  'time.observation': '2016-12-08T07:57:36+00:00',
                  'raw': utils.base64_encode(EXAMPLE_FILE)
                  }

EXAMPLE_EVENT = [{'feed.name': 'Proxy Spy',
                  'feed.url': 'http://txt.proxyspy.net/proxy.txt',
                  '__type': 'Event',
                  'time.observation': '2016-12-08T07:57:36+00:00',
                  'raw': 'MTc4LjI1My4yMTcuMTMxOjY2NjYgUlMtTi1TICs=',
                  'time.source': '2016-12-08T10:55:02+00:00',
                  'source.ip': '178.253.217.131',
                  'source.port': 6666,
                  'source.geolocation.cc': 'RS',
                  'event_description.text': 'Possible HTTP/HTTPS proxy usage when IP and port match '
                                            'for outbound traffic.',
                  'classification.type': 'proxy'
                  },
                 {'feed.name': 'Proxy Spy',
                  'feed.url': 'http://txt.proxyspy.net/proxy.txt',
                  '__type': 'Event',
                  'time.observation': '2016-12-08T07:57:36+00:00',
                  'raw': 'OTYuMjM0LjQzLjEzNDo4MCBVUy1IIC0=',
                  'time.source': '2016-12-08T10:55:02+00:00',
                  'source.ip': '96.234.43.134',
                  'source.port': 80,
                  'source.geolocation.cc': 'US',
                  'event_description.text': 'Possible HTTP/HTTPS proxy usage when IP and port match '
                                            'for outbound traffic.',
                  'classification.type': 'proxy'
                  }]

class TestProxyspyParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for ProxyspyParserBot """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ProxyspyParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_bot(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT[0])
        self.assertMessageEqual(1, EXAMPLE_EVENT[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
