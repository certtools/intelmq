# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.reverse_dns.expert import ReverseDnsExpertBot
from intelmq.lib.cache import Cache

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


class TestReverseDnsExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ReverseDnsExpertBot
        cls.default_input_message = {'__type': 'Report'}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    @classmethod
    def tearDownClass(cls):
        cache = Cache(test.BOT_CONFIG['redis_cache_host'],
                      test.BOT_CONFIG['redis_cache_port'],
                      test.BOT_CONFIG['redis_cache_db'],
                      test.BOT_CONFIG['redis_cache_ttl'],
                      )
        cache.flush()

if __name__ == '__main__':
    unittest.main()
