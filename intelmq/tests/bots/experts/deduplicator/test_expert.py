# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.message as message
import intelmq.lib.test as test
from intelmq.bots.experts.deduplicator.expert import DeduplicatorExpertBot

INPUT1 = {"__type": "Event",
          "classification.identifier": "zeus",
          "source.ip": "192.0.2.1",
          "time.observation": '2015-01-01T13:37:00+00:00',
          }
INPUT2 = INPUT1.copy()
INPUT2['source.ip'] = '192.168.0.4'


@test.skip_redis()
class TestDeduplicatorExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DeduplicatorExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DeduplicatorExpertBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"redis_cache_ttl": "86400",
                         "filter_type": "blacklist",
                         "filter_keys": "raw ,time.observation "}
        cls.use_cache = True

    def test_suppress(self):
        msg = message.MessageFactory.from_dict(INPUT1, harmonization=self.harmonization)
        msg_hash = hash(msg)
        self.cache.set(msg_hash, 'hash')
        self.cache.expire(msg_hash, 3600)
        self.run_bot()
        self.assertOutputQueueLen()

    def test_pass(self):
        self.input_message = INPUT2
        self.run_bot()
        self.assertMessageEqual(0, INPUT2)

    def test_old_hash(self):
        self.cache.flushdb()
        self.cache.set(1241421362111650194, 'hash')
        self.cache.expire(1241421362111650194, 3600)
        self.run_bot()
        self.assertOutputQueueLen()

    def test_whitelist_suppress(self):
        self.sysconfig = {"redis_cache_ttl": "86400",
                          "filter_type": "whitelist",
                          "filter_keys": "source.ip"}
        msg = self.new_event()
        msg.add('source.ip', '127.0.0.8')
        msg_hash = hash(msg)
        self.cache.set(msg_hash, 'hash')
        self.cache.expire(msg_hash, 3600)

        msg.add('destination.ip', '127.0.0.7')
        self.input_message = msg
        self.run_bot()
        self.assertOutputQueueLen()

    def test_whitelist_pass(self):
        self.sysconfig = {"redis_cache_ttl": "86400",
                          "filter_type": "whitelist",
                          "filter_keys": "source.ip"}
        msg = self.new_event()
        msg.add('destination.ip', '127.0.0.7')
        self.input_message = msg
        self.run_bot()
        self.assertMessageEqual(0, msg)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
