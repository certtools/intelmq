# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.cymru_whois.expert import CymruExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "78.104.144.2",  # example.com
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "78.104.144.2",
                  "source.geolocation.cc": "AT",
                  "source.registry": "RIPE",
                  "source.network": "78.104.0.0/16",
                  "source.allocated": "2007-06-07T00:00:00+00:00",
                  "source.asn": 1853,
                  "source.as_name": "ACONET ACOnet Backbone, AT",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "destination.ip": "2001:500:88:200::8",  # iana.org
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "destination.ip": "2001:500:88:200::8",  # iana.org
                   "destination.registry": "ARIN",
                   "destination.allocated": "2010-02-18T00:00:00+00:00",
                   "destination.as_name": "ICANN-DC, US",
                   "destination.geolocation.cc": "US",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "destination.asn": 16876,
                   "destination.network": "2001:500:88::/48",
                   }
EMPTY_INPUT = {"__type": "Event",
               "source.ip": "127.0.0.1",  # no result
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
EXAMPLE_6TO4_INPUT = {"__type": "Event",
                 "source.ip": "2002:3ee0:3972:0001::1",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_6TO4_OUTPUT = {"__type": "Event",
                  "source.ip": "2002:3ee0:3972:0001::1",
                  "source.network": "2002::/16",
                  "source.asn": 1103,
                  "source.as_name": "SURFNET-NL SURFnet, The Netherlands, NL",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_6TO4_OUTPUT_1 = {"__type": "Event",
                  "source.ip": "2002:3ee0:3972:0001::1",
                  "source.network": "2002::/16",
                  "source.asn": 6939,
                  "source.as_name": "HURRICANE, US",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
OVERWRITE_OUT = {"__type": "Event",
                  "source.ip": "78.104.144.2",
                  "source.geolocation.cc": "AA",
                  "source.registry": "LACNIC",
                  "source.network": "78.104.0.0/16",
                  "source.allocated": "2007-06-07T00:00:00+00:00",
                  "source.asn": 1853,
                  "source.as_name": "ACONET ACOnet Backbone, AT",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


@test.skip_redis()
@test.skip_internet()
@test.skip_ci()
class TestCymruExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CymruExpertBot
        cls.use_cache = True
        cls.sysconfig = {'overwrite': True}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    def test_empty_result(self):
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)

    def test_6to4_result(self):
        """
        Test the whois for an IPv6 to IPv4 network range.
        The result can vary, so we test for two possible expected results.
        """
        self.input_message = EXAMPLE_6TO4_INPUT
        self.run_bot()
        try:
            self.assertMessageEqual(0, EXAMPLE_6TO4_OUTPUT)
        except AssertionError:
            self.assertMessageEqual(0, EXAMPLE_6TO4_OUTPUT_1)

    def test_overwrite(self):
        self.input_message = EXAMPLE_INPUT.copy()
        self.input_message["source.geolocation.cc"] = "AA"
        self.input_message["source.registry"] = "LACNIC"
        self.run_bot(parameters={'overwrite' : False})
        self.assertMessageEqual(0, OVERWRITE_OUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
