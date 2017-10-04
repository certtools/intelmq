# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.source": "2005-01-01T00:00:00+00:00",
                 "source.asn": 123,
                 "extra.test1": True,
                 "extra.test2": "bla",
                 }


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
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

    def test_extra_filter_keep(self):
        self.sysconfig = {'filter_key': 'extra.test2',
                         'filter_value': 'bla',
                         'filter_action': 'keep'}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
