# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.ripencc_abuse_contact.expert import RIPENCCExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "193.238.157.5",  # funkfeuer.at
                 "destination.asn": 35492,
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.abuse_contact": "abuse@verizondigitalmedia.com",
                  "destination.ip": "193.238.157.5",
                  "destination.abuse_contact": "abuse@funkfeuer.at",
                  "destination.asn": 35492,
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:62a:4:100:80::8",  # nic.at
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:62a:4:100:80::8",
                   "source.abuse_contact": "security.zid@univie.ac.at",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }


@test.skip_internet()
class TestRIPENCCExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RIPENCCExpertBot
        cls.sysconfig = {'query_ripe_db_asn': True,
                         'query_ripe_db_ip': True,
                         'query_ripe_stat': True,
                         }

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
