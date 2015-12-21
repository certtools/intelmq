# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.lib.cache import Cache
from intelmq.bots.experts.forward_dns.expert import ForwardDnsExpertBot

EXAMPLE_INPUT = {"__type": "Event",                 
                 "source.fqdn": "icann.org",
                 "destination.fqdn": "iana.org",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",                  
                  "source.fqdn": "icann.org",
                  "destination.fqdn": "iana.org",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "source.ip": "2001:500:88:200::7"
                  #"source.forward_dns": "2001:500:88:200::72001:500:88:200::72001:500:88:200::7192.0.43.7192.0.43.7192.0.43.7",
                  #"destination.forward_dns": '2001:500:88:200::82001:500:88:200::82001:500:88:200::8192.0.43.8192.0.43.8192.0.43.8',
                  #"time.observation": "2015-01-01T00:00:00+00:00",
                  }


class TestForwardDnsExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = ForwardDnsExpertBot
        self.default_input_message = {'__type': 'Report'}

    def test_ip_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

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
