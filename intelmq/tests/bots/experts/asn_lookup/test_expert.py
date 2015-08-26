# -*- coding: utf-8 -*-
"""
Testing asn_lookup.

see asn_lookup README for how to download database
It is expected at /opt/intelmq/var/lib/bots/asn_lookup/ipasn.dat by default
"""
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.asn_lookup.expert import ASNLookupExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "192.0.43.8",  # iana.org
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.asn": "15133",
                  "source.bgp_prefix": "93.184.216.0/24",
                  "destination.ip": "192.0.43.8",
                  "destination.asn": "16876",
                  "destination.bgp_prefix": "192.0.43.0/24",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::7",  # iana.org
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "source.asn": "16876",
                   "source.bgp_prefix": "2001:500:88::/48",
                   }


class TestASNLookupExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = ASNLookupExpertBot
        self.sysconfig = {'database': '/opt/intelmq/var/lib/bots/asn_lookup/'
                                      'ipasn.dat'}
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
