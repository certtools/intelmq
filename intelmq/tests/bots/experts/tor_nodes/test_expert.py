# -*- coding: utf-8 -*-
"""
Testing asn_lookup.

TODO: IPv6
"""
from __future__ import unicode_literals

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.tor_nodes.expert import TorExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "37.130.227.133",
                 "destination.ip": "192.0.43.8",  # iana.org
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "37.130.227.133",
                  "source.tor_node": "true",
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


class TestTorExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = TorExpertBot
        self.sysconfig = {'database': '/opt/intelmq/var/lib/bots/tor_nodes/'
                                      'tor_nodes.dat'}
        self.default_input_message = json.dumps({'__type': 'Report'})

    def test_ipv4_lookup(self):
        self.input_message = json.dumps(EXAMPLE_INPUT)
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

if __name__ == '__main__':
    unittest.main()
