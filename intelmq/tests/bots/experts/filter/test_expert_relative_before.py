# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.source": "2005-01-01T00:00:00+00:00",
                 "time.observation": "2015-09-12T00:00:00+00:00",
                 "feed.name": "test-feed",
                 "raw": "fds56gf4jh4jhgh4j6"
                 }


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilterExpertBot
        cls.input_message = EXAMPLE_INPUT
        ''' this test will fail in 20 years from now :( '''
        cls.sysconfig = {'not_before': '30 years'}

    def test_Relative_Before(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT)

if __name__ == '__main__':
    unittest.main()
