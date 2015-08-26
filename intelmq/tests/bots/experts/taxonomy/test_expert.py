# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.taxonomy.expert import TaxonomyExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "defacement",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "classification.type": "defacement",
                  "classification.taxonomy": "Intrusions",
                  }


class TestTaxonomyExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = TaxonomyExpertBot
        self.default_input_message = json.dumps({'__type': 'Report'})

    def test_classification(self):
        self.input_message = json.dumps(EXAMPLE_INPUT)
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main()
