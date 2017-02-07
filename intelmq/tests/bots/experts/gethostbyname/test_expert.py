# -*- coding: utf-8 -*-
"""
Testing GethostbynameExpertBot.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.gethostbyname.expert import GethostbynameExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.fqdn": "example.com",
                 "destination.fqdn": "example.org",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.fqdn": "example.com",
                  "destination.fqdn": "example.org",
                  "source.ip": "93.184.216.34",
                  "destination.ip": "93.184.216.34",
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }
NONEXISTING_INPUT = {"__type": "Event",
                     "source.fqdn": "example.invalid",
                     "destination.fqdn": "example.invalid",
                     "time.observation": "2015-01-01T00:00:00+00:00"
                     }


@test.skip_internet()
class TestGethostbynameExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for GethostbynameExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = GethostbynameExpertBot

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
