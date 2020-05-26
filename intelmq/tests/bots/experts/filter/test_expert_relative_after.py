# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.source": "2005-01-01T00:00:00+00:00",
                 "time.observation": "2015-09-12T00:00:00+00:00",
                 "feed.name": "test-feed",
                 }


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilterExpertBot
        cls.input_message = EXAMPLE_INPUT
        cls.sysconfig = {'not_after': '1 month'}

    def test_Relative_After(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT)

    def test_bug_1523(self):
        """
        > For relative filter, if param not_after: x hours (x < 24) is given, instead of being parsed as datetime.timedelta
        > ...
        > Leading to error
        > TypeError: can't compare offset-naive and offset-aware datetimes
        https://github.com/certtools/intelmq/issues/1523
        """
        self.run_bot(parameters={'not_after': '10 hours'})
        self.assertMessageEqual(0, EXAMPLE_INPUT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
