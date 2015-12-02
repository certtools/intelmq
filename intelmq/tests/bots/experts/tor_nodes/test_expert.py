# -*- coding: utf-8 -*-
"""
Testing asn_lookup.

TODO: IPv6
"""
from __future__ import unicode_literals

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.tor_nodes.expert import TorExpertBot

TOR_DB = '/opt/intelmq/var/lib/bots/tor_nodes/tor_nodes.dat'
EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "37.130.227.133",
                 "destination.ip": "192.0.43.8",  # iana.org
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "37.130.227.133",
                  "source.tor_node": True,
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


@unittest.skipUnless(os.path.exists(TOR_DB), 'tor-nodes database does not'
                                             'exist in {}.'.format(TOR_DB))
class TestTorExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = TorExpertBot
        self.sysconfig = {'database': TOR_DB}
        self.default_input_message = {'__type': 'Report'}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

if __name__ == '__main__':
    unittest.main()
