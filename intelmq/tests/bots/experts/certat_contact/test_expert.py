# -*- coding: utf-8 -*-
"""
Testing certat_contact
"""
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.certat_contact.expert import CERTatContactExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "83.136.38.146",  # cert.at
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.geolocation.cc": "US",
                  "source.abuse_contact": "soc@us-cert.gov",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "destination.ip": "83.136.38.146",
                  "destination.geolocation.cc": "AT",
                  "destination.abuse_contact": "reports@cert.at",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::7",  # iana.org
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "source.abuse_contact": "existing@example.com",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::7",
                   "source.abuse_contact": "existing@example.com,soc@us-cert.gov",
                   "source.geolocation.cc": "US",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }


@test.skip_internet()
class TestCERTatContactExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CERTatContactExpertBot
        cls.sysconfig = {'filter': False,
                         'overwrite_cc': False,
                         'http_verify_cert': False,
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
