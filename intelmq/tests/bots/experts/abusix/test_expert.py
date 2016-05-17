# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.abusix.expert import AbusixExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.0.43.7",  # icann.org
                 "destination.ip": "192.0.43.8",  # iana.org
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.0.43.7",
                  "destination.ip": "192.0.43.8",
                  "source.abuse_contact": "ops@icann.org",
                  "destination.abuse_contact": "ops@icann.org",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::7",  # iana.org
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "source.abuse_contact": "ops@icann.org",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }


class TestAbusixExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusixExpertBot
        cls.default_input_message = {'__type': 'Report'}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

if __name__ == '__main__':
    unittest.main()
