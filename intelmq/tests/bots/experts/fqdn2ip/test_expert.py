# -*- coding: utf-8 -*-
"""
Testing Fqdn2Ip.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.fqdn2ip.expert import Fqdn2IpExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.fqdn": "example.com",
                 "destination.fqdn": "example.org",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.fqdn": "example.com",
                  "destination.fqdn": "example.org",
                  "source.ip": "",
                  "destination.ip": "93.184.216.34",
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }


class TestFqdn2IpExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Fqdn2IpExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = Fqdn2IpExpertBot
        self.default_input_message = {'__type': 'Event'}

    def test(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

if __name__ == '__main__':
    unittest.main()
    
