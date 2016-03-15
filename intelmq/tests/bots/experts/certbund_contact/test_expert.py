# -*- coding: utf-8 -*-

"""
Testing certbund_contact
"""

from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.certbund_contact.expert import CERTBundKontaktExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.168.42.23",
                 "destination.ip": "192.168.42.47",
                 "time.observation": "2016-02-26T10:11:12+00:00"
                 }

EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.168.42.23",
                  "source.abuse_contact": "foo@example.com",
                  "destination.ip": "192.168.42.47",
                  "destination.abuse_contact": "foo@example.com",
                  "time.observation": "2016-02-26T10:11:12+00:00"
                  }

class CERTBundKontaktMockDBExpertBot(CERTBundKontaktExpertBot):

    """CERTBundKontaktExpertBot that does not mocks all database accesses"""

    def connect_to_database(self):
        pass

    def lookup_ip(self, ip):
        if ip.startswith("192.168.42."):
            return ["foo@example.com"]
        return None


class TestCERTBundKontaktMockDBExpertBot(test.BotTestCase, unittest.TestCase):

    """
    A TestCase for CERTBundKontaktExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CERTBundKontaktMockDBExpertBot

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == "__main__":
    unittest.main()
