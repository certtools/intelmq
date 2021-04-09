# -*- coding: utf-8 -*-
"""
Testing url2fqdn.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.rdap.expert import RDAPExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://nic.versicherung/something/index.php",
                 "source.fqdn": "nic.versicherung",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.url": "http://nic.versicherung/something/index.php",
                  "source.fqdn": "nic.versicherung",
                  "source.abuse_contact": 'service@tld-box.at',
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }


@test.skip_internet()
class TestRDAPExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RDAPExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = RDAPExpertBot

    def test(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
