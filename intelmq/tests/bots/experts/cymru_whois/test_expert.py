# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.cymru_whois.expert import CymruExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.geolocation.cc": "EU",
                  "source.registry": "RIPE",
                  "source.network": "93.184.216.0/24",
                  "source.allocated": "2008-06-02T00:00:00+00:00",
                  "source.asn": 15133,
                  "source.as_name": "EDGECAST - MCI Communications Services, Inc. d/b/a Verizon Business, US",
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
                   "destination.as_name": "ICANN-DC - ICANN, US",
                   "destination.geolocation.cc": "US",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "destination.asn": 16876,
                   "destination.network": "2001:500:88::/48",
                   }
UNICODE_INPUT = {"__type": "Event",
                 "destination.ip": "200.236.128.1",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
UNICODE_OUTPUT = {"__type": "Event",
                  "destination.ip": "200.236.128.1",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "destination.registry": "LACNIC",
                  "destination.allocated": "2000-02-15T00:00:00+00:00",
                  "destination.as_name": "Fundação de Desenvolvimento da Pesquisa, BR",
                  "destination.geolocation.cc": "BR",
                  "destination.asn": 10417,
                  "destination.network": "200.236.128.0/18",
                  }
EMPTY_INPUT = {"__type": "Event",
               "source.ip": "198.105.125.77",  # no result
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
NO_ASN_INPUT = {"__type": "Event",
                "source.ip": "212.92.127.126",
                "time.observation": "2015-01-01T00:00:00+00:00",
                }
NO_ASN_OUTPUT = {"__type": "Event",
                 "source.ip": "212.92.127.126",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "source.asn": 23456,
                 "source.geolocation.cc": 'RU',
                 "source.ip": '212.92.127.126',
                 "source.network": '212.92.127.0/24',
                 "source.registry": 'RIPE',
                 }


@test.skip_redis()
@test.skip_internet()
class TestCymruExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CymruExpertBot
        cls.use_cache = True

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    def test_unicode_as_name(self):
        self.input_message = UNICODE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, UNICODE_OUTPUT)

    def test_empty_result(self):
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)

    @unittest.expectedFailure
    def test_missing_asn(self):
        """
        No information for ASN.

        https://github.com/certtools/intelmq/issues/635
        """
        self.input_message = NO_ASN_INPUT
        self.run_bot()
        self.assertMessageEqual(0, NO_ASN_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
