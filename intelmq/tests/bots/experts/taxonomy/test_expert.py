# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.taxonomy.expert import TaxonomyExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "classification.type": "defacement",
                  "classification.taxonomy": "Intrusions",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


class TestTaxonomyExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TaxonomyExpertBot

    def test_classification(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
