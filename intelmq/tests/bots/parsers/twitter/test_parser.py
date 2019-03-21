# -*- coding: utf-8 -*-

import os
import sys
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.twitter.parser import TwitterParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'tweet.txt')) as handle:
    EXAMPLE_FILE = handle.read()

REPORT = {'__type': 'Report',
          'feed.name': 'Twitter',
          'feed.url': 'https://twitter.com/El_carlos/1234456',
          'raw': utils.base64_encode(EXAMPLE_FILE),
          'time.observation': '2015-09-14T12:00:00+02:00'
          }
EVENTS =[ {'source.url': 'http://testweb.com/sales-invoice/',
            '__type': 'Event',
          'feed.name': 'Twitter',
          'classification.type':'blacklist',
          'feed.url': 'https://twitter.com/El_carlos/1234456',
          'time.observation': '2015-09-14T12:00:00+02:00',
          'raw': utils.base64_encode(EXAMPLE_FILE)},
            {'source.url': 'http://cc.pro/images.html',
            '__type': 'Event',
          'feed.name': 'Twitter',
          'classification.type':'blacklist',
          'feed.url': 'https://twitter.com/El_carlos/1234456',
          'time.observation': '2015-09-14T12:00:00+02:00',
          'raw': utils.base64_encode(EXAMPLE_FILE)},
            {'source.url': 'http://karlos.net/',
            '__type': 'Event',
          'feed.name': 'Twitter',
          'classification.type':'blacklist',
          'feed.url': 'https://twitter.com/El_carlos/1234456',
          'time.observation': '2015-09-14T12:00:00+02:00',
          'raw': utils.base64_encode(EXAMPLE_FILE)},
            {'source.url': 'http://block.de.com/malware.exe',
            '__type': 'Event',
          'feed.name': 'Twitter',
          'classification.type':'blacklist',
          'feed.url': 'https://twitter.com/El_carlos/1234456',
          'time.observation': '2015-09-14T12:00:00+02:00',
          'raw': utils.base64_encode(EXAMPLE_FILE)},
            {'source.url': 'http://ghzz.com/',
            '__type': 'Event',
          'feed.name': 'Twitter',
          'classification.type':'blacklist',
          'feed.url': 'https://twitter.com/El_carlos/1234456',
          'time.observation': '2015-09-14T12:00:00+02:00',
          'raw': utils.base64_encode(EXAMPLE_FILE)}]


@test.skip_exotic()
class TestTwitterParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TwitterParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TwitterParserBot
        cls.sysconfig = {"substitutions" : " .net;.net;[.];.;,;.",
                         "classification_type": "blacklist",
                         }
        if sys.version_info >= (3, 6, 0):
            # url-normalize 1.4.1 supporting this parameter is only available for 3.6
            cls.sysconfig["default_scheme"] = "http"

    def test_parse(self):
        self.input_message = REPORT
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])
        self.assertMessageEqual(1, EVENTS[1])
        self.assertMessageEqual(2, EVENTS[2])
        self.assertMessageEqual(3, EVENTS[3])
        self.assertMessageEqual(4, EVENTS[4])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
