# -*- coding: utf-8 -*-
"""
Testing GethostbynameExpertBot.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.domaintools.expert import DomaintoolsExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.fqdn": "google.com",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.fqdn": "google.com",
                  "extra": '{"domaintools_score": 0}',
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }
NONEXISTING_INPUT = {"__type": "Event",
                     "source.fqdn": "example.invalid",
                     "destination.fqdn": "example.invalid",
                     "time.observation": "2015-01-01T00:00:00+00:00"
                     }


@test.skip_internet()
class TestDomaintoolsExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DomaintoolsExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = DomaintoolsExpertBot
        self.sysconfig = {'user': 'mkendrick_first2017', 'password': 'c0e4e-e2527-dc6af-824a4-229d5'}

    def test_existing(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_non_existing(self):
        self.input_message = NONEXISTING_INPUT
        self.run_bot()
        self.assertMessageEqual(0, NONEXISTING_INPUT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
