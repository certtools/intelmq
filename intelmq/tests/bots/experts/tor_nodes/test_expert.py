# -*- coding: utf-8 -*-
"""
Testing tor node lookup
"""

import unittest

import pkg_resources

import intelmq.lib.test as test
from intelmq.bots.experts.tor_nodes.expert import TorExpertBot

TOR_DB = pkg_resources.resource_filename('intelmq', 'tests/bots/experts/tor_nodes/tor_nodes.dat')
EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.168.0.1",
                 "destination.ip": "192.0.43.8",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.168.0.1",
                  "source.tor_node": True,
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EMPTY = {"__type": "Event",
                 "source.ip": "10.0.0.1",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }


class TestTorExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TorExpertBot
        cls.sysconfig = {'database': TOR_DB}

    def test_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_empty_lookup(self):
        self.input_message = EXAMPLE_EMPTY
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EMPTY)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
