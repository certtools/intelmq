# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot

EXAMPLE_INPUT = {"__type": "Report",
                 "raw": "Cg==",
                 "extra.test1": True,
                 "extra.test2": "bla",
                 }
EXAMPLE_INPUT1 = {"__type": "Report",
                  "raw": "Cg==",
                  "extra.test1": False,
                  }


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot handling Reports.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilterExpertBot
        cls.input_message = EXAMPLE_INPUT
        cls.sysconfig = {'filter_key': 'extra.test1',
                         'filter_value': True,
                         'filter_action': 'drop'}

    def test_extra_filter_drop(self):
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_extra_filter_keep(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
