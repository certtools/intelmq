# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.reverse_dns.expert import ReverseDnsExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.0.43.7",  # icann.org
                 "destination.ip": "192.0.43.8",  # iana.org
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.0.43.7",
                  "source.reverse_dns": "icann.org",
                  "destination.ip": "192.0.43.8",
                  "destination.reverse_dns": "icann.org",
                  # manual verfication shows another result:
                  # "destination.reverse_dns": "43-8.any.icann.org",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:500:88:200::8",  # iana.org
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:500:88:200::8",
                   "source.reverse_dns": "iana.org",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }
INVALID_PTR_INP = {"__type": "Event",
                   "source.ip": "31.210.115.39",  # PTR is '.'
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }
INVALID_PTR_OUT = {"__type": "Event",
                   "source.ip": "31.210.115.39",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }
INVALID_PTR_INP2 = {"__type": "Event",
                    "source.ip": "5.157.80.221",  # PTR is '5.157.80.221.' and 'aliancys.peopleinc.nl.'
                    "time.observation": "2015-01-01T00:00:00+00:00",
                    }
INVALID_PTR_OUT2 = {"__type": "Event",
                    "source.ip": "5.157.80.221",
                    "source.reverse_dns": "aliancys.peopleinc.nl",
                    "time.observation": "2015-01-01T00:00:00+00:00",
                    }


@test.skip_redis()
@test.skip_internet()
class TestReverseDnsExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ReverseDnsExpertBot
        cls.use_cache = True

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    def test_invalid_ptr(self):
        self.input_message = INVALID_PTR_INP
        self.run_bot()
        self.assertMessageEqual(0, INVALID_PTR_OUT)

    def test_invalid_ptr2(self):
        self.input_message = INVALID_PTR_INP2
        self.run_bot()
        self.assertMessageEqual(0, INVALID_PTR_OUT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
