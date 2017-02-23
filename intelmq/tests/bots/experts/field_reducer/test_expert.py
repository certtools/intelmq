# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.field_reducer.expert import FieldReducerExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.observation": "2015-09-12T00:00:00+00:00",
                 "feed.name": "test-feed",
                 }
WHITELIST_OUTPUT = {"__type": "Event",
                    "time.observation": "2015-09-12T00:00:00+00:00",
                    }
BLACKLIST_OUTPUT = {"__type": "Event",
                    "classification.type": "defacement",
                    "feed.name": "test-feed",
                    }


class TestFieldReducerExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FieldReducerExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FieldReducerExpertBot
        cls.input_message = EXAMPLE_INPUT
        cls.sysconfig = {'type': 'whitelist', 'keys': ['time.source', 'time.observation']}

    def test_whitelist(self):
        self.run_bot()
        self.assertMessageEqual(0, WHITELIST_OUTPUT)

    def test_blacklist(self):
        self.sysconfig = {'type': 'blacklist', 'keys': 'time.source, time.observation'}
        self.run_bot()
        self.assertMessageEqual(0, BLACKLIST_OUTPUT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
