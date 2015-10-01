# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.source": "2015-01-01T00:00:00+00:00",
                 "time.observation": "2015-09-012T00:00:00+00:00",
                 "feed.name": "test-feed",
                 "raw": "fds56gf4jh4jhgh4j6"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "classification.type": "defacement",
                  "time.source": "2015-01-01T00:00:00+00:00",
                  "time.observation": "2015-09-012T00:00:00+00:00",
                  "feed.name": "test-feed",
                  "raw": "fds56gf4jh4jhgh4j6"
                  }


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = FilterExpertBot
        self.sysconfig = {'not_before': '2014-01-01T00:00:00+00:00', 
                          'not_after': '6 months'}
        self.input_message = EXAMPLE_INPUT

    def test_Filter(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main()
