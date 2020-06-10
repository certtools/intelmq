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
QUEUES = {"_default", "action_other", "filter_match", "filter_no_match"}


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilterExpertBot
        cls.input_message = EXAMPLE_INPUT
        cls.sysconfig = {'filter_key': 'classification.type',
                         'filter_value': "defacement",
                         'filter_action': 'drop'}

    def test_extra_filter_drop(self):
        self.prepare_bot(destination_queues=QUEUES, parameters={'logging_level': 'DEBUG'})
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0, path="_default")
        self.assertLogMatches(".*Sending message to path 'filter_match'.",
                              levelname='DEBUG')
        self.assertMessageEqual(0, EXAMPLE_INPUT, path="filter_match")
        self.assertOutputQueueLen(0, path="filter_no_match")
        self.assertLogMatches(".*Sending message to path 'action_other'.",
                              levelname='DEBUG')
        self.assertMessageEqual(0, EXAMPLE_INPUT, path="action_other")

    def test_extra_filter_keep(self):
        self.prepare_bot(destination_queues=QUEUES,
                         parameters={'filter_key': 'extra.test2',
                                     'filter_value': 'bla',
                                     'filter_action': 'keep',
                                     'logging_level': 'DEBUG'})
        self.run_bot(prepare=False)
        self.assertLogMatches(".*Sending message to path '_default'.",
                              levelname='DEBUG')
        self.assertLogMatches(".*Sending message to path 'filter_match'.",
                              levelname='DEBUG')
        self.assertMessageEqual(0, EXAMPLE_INPUT)
        self.assertMessageEqual(0, EXAMPLE_INPUT, path="filter_match")
        self.assertOutputQueueLen(0, path="filter_no_match")
        self.assertOutputQueueLen(0, path="action_other")

    def test_filter_no_match_keep(self):
        self.prepare_bot(destination_queues=QUEUES,
                         parameters={'filter_key': 'extra.test2',
                                     'filter_value': 'foo',
                                     'filter_action': 'keep',
                                     'logging_level': 'DEBUG'})
        self.run_bot(prepare=False)
        self.assertLogMatches(".*Sending message to path 'action_other'.",
                              levelname='DEBUG')
        self.assertMessageEqual(0, EXAMPLE_INPUT, path="action_other")
        self.assertLogMatches(".*Sending message to path 'filter_no_match'.",
                              levelname='DEBUG')
        self.assertMessageEqual(0, EXAMPLE_INPUT, path="filter_no_match")
        self.assertOutputQueueLen(0, path="filter_match")
        self.assertOutputQueueLen(0)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
