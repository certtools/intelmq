# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import unittest

import intelmq.lib.harmonization as harmonization
import intelmq.lib.message as message
import intelmq.lib.test as test
from intelmq.bots.experts.deduplicator.expert import DeduplicatorExpertBot


INPUT1 = {"__type": "Event",
          "classification.identifier": "zeus",
          "source.ip": "192.0.2.1",
          "time.observation": harmonization.DateTime.generate_datetime_now(),
          }
INPUT2 = INPUT1.copy()
INPUT2['source.ip'] = '192.168.0.4'


class TestDeduplicatorExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DeduplicatorExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DeduplicatorExpertBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"redis_cache_ttl": "86400",
                         "ignore_keys": "raw ,time.observation "}
        cls.redis = redis.Redis(host=test.BOT_CONFIG['redis_cache_host'],
                                port=test.BOT_CONFIG['redis_cache_port'],
                                db=test.BOT_CONFIG['redis_cache_db'],
                                socket_timeout=5)
        cls.redis.flushdb()

    def test_suppress(self):
        msg = message.MessageFactory.from_dict(INPUT1)
        msg_hash = hash(msg)
        self.redis.set(msg_hash, 'hash')
        self.redis.expire(msg_hash, 3600)
        self.input_message = INPUT1
        self.run_bot()
        self.assertOutputQueueLen()

    def test_pass(self):
        self.input_message = INPUT2
        self.run_bot()
        self.assertMessageEqual(0, INPUT2)

    @classmethod
    def tearDownClass(cls):
        cls.redis.flushdb()


if __name__ == '__main__':
    unittest.main()
