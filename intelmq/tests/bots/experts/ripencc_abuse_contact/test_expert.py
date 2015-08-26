# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.ripencc_abuse_contact.expert import RIPENCCExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "192.0.43.8",  # iana.org, not in RIPENCC
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.abuse_contact": "abuse@edgecast.com",
                  "destination.ip": "192.0.43.8",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",  # example.com
                  "source.ip": "2606:2800:220:1:248:1893:25c8:1946",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "source.abuse_contact": "abuse@edgecast.com",
                   }


class TestRIPENCCExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = RIPENCCExpertBot
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
