# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.abusix.expert import AbusixExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "192.0.43.8",  # iana.org
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "destination.ip": "192.0.43.8",
                  "source.abuse_contact": "abuse@edgecast.com",
                  "destination.abuse_contact": "ops@icann.org",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::7",  # iana.org
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "source.abuse_contact": "ops@icann.org",
                   }


class TestAbusixExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = AbusixExpertBot
        self.default_input_message = json.dumps({'__type': 'Report'})

    def test_ipv4_lookup(self):
        self.input_message = json.dumps(EXAMPLE_INPUT)
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_OUTPUT)

    @unittest.expectedFailure
    def test_ipv6_lookup(self):
        self.input_message = json.dumps(EXAMPLE_INPUT6)
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_OUTPUT6)

if __name__ == '__main__':
    unittest.main()
