# -*- coding: utf-8 -*-
"""
Testing url2fqdn.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.url2fqdn.expert import Url2fqdnExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://example.com/something/index.php",
                 "destination.url": "http://example.org/download?file.exe",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.url": "http://example.com/something/index.php",
                  "destination.url": "http://example.org/download?file.exe",
                  "source.fqdn": "example.com",
                  "destination.fqdn": "example.org",
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }


class TestUrl2fqdnExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Url2fqdnExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = Url2fqdnExpertBot

    def test(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_overwrite(self):
        self.input_message = EXAMPLE_INPUT.copy()
        self.input_message['source.fqdn'] = 'example.net'
        self.sysconfig = {'overwrite' : True}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
