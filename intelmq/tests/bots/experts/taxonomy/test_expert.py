# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.taxonomy.expert import TaxonomyExpertBot, TAXONOMY
from intelmq.lib.harmonization import ClassificationType


EXAMPLE_INPUT1 = {"__type": "Event",
                 "classification.type": "defacement",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                  "classification.type": "defacement",
                  "classification.taxonomy": "intrusions",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT2 = {"__type": "Event",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                  "classification.type": "unknown",
                  "classification.taxonomy": "other",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT3 = {"__type": "Event",
                 "classification.taxonomy": "vulnerable",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT3 = {"__type": "Event",
                 "classification.taxonomy": "vulnerable",
                  "classification.type": "unknown",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT4 = {"__type": "Event",
                 "classification.taxonomy": "vulnerable",
                  "classification.type": "unknown",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT4 = {"__type": "Event",
                 "classification.taxonomy": "vulnerable",
                  "classification.type": "unknown",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


class TestTaxonomyExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TaxonomyExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TaxonomyExpertBot

    def test_classification(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)
        self.input_message = EXAMPLE_INPUT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)
        self.input_message = EXAMPLE_INPUT3
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)
        self.input_message = EXAMPLE_INPUT4
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT4)


class TestHarmonization(unittest.TestCase):
    def test_classification_coverage(self):
        """
        Assert that the types list in the taxonomy expert is the same as in the harmonization.
        """
        intelmq_harmonization = set(ClassificationType.allowed_values)
        taxonomy_expert = set(TAXONOMY.keys())
        self.assertSetEqual(intelmq_harmonization, taxonomy_expert)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
