# -*- coding: utf-8 -*-

import json
import os
import unittest

import redis

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.outputs.redis.output import RedisOutputBot

EXAMPLE_EVENT = {"classification.type": "malware",
                 "destination.port": 9796,
                 "feed.accuracy": 100.0,
                 "destination.ip": "52.18.196.169",
                 "malware.name": "salityp2p",
                 "event_description.text": "Sinkhole attempted connection",
                 "time.source": "2016-04-19T23:16:08+00:00",
                 "source.ip": "152.166.119.2",
                 "feed.url": "http://alerts.bitsighttech.com:8080/stream?",
                 "source.geolocation.country": "Dominican Republic",
                 "time.observation": "2016-04-19T23:16:08+00:00",
                 "source.port": 65118,
                 "__type": "Event",
                 "feed.name": "BitSight",
                 "extra.non_ascii": "ççãããã\x80\ua000 \164 \x80\x80 abcd \165\166",
                 "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTYWxpdHlwMnAiLCJlbnYiOnsic"
                 "mVtb3RlX2FkZHIiOiIxNTIuMTY2LjExOS4yIiwicmVtb3RlX3"
                 "BvcnQiOiI2NTExOCIsInNlcnZlcl9hZGRyIjoiNTIuMTguMTk"
                 "2LjE2OSIsInNlcnZlcl9wb3J0IjoiOTc5NiJ9LCJfdHMiOjE0"
                 "NjExMDc3NjgsIl9nZW9fZW52X3JlbW90ZV9hZGRyIjp7ImNvd"
                 "W50cnlfbmFtZSI6IkRvbWluaWNhbiBSZXB1YmxpYyJ9fQ=="
                 }


class TestRedisOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RedisOutputBot
        cls.default_input_message = EXAMPLE_EVENT
        cls.sysconfig = {"redis_server_ip": "127.0.0.1",
                         "redis_server_port": 6379,
                         "redis_db": 4,
                         "redis_queue": "test-redis-output-queue",
                         "redis_password": os.getenv('INTELMQ_TEST_REDIS_PASSWORD'),
                         "redis_timeout": "50000"}

    @test.skip_redis()
    def test_event(self):
        """ Setup Redis connection """
        redis_ip = self.sysconfig['redis_server_ip']
        redis_port = self.sysconfig['redis_server_port']
        redis_db = self.sysconfig['redis_db']
        redis_queue = self.sysconfig['redis_queue']
        redis_password = self.sysconfig['redis_password']
        redis_timeout = self.sysconfig['redis_timeout']
        redis_conn = redis.ConnectionPool(host=redis_ip, port=redis_port,
                                          db=redis_db, password=redis_password)
        redis_version = tuple(int(x) for x in redis.__version__.split('.'))
        if redis_version >= (3, 0, 0):
            redis_class = redis.Redis
        else:
            redis_class = redis.StrictRedis
        redis_output = redis_class(connection_pool=redis_conn,
                                   socket_timeout=redis_timeout,
                                   password=redis_password)

        self.run_bot()

        # Get the message from Redis
        event = utils.decode(redis_output.lpop(redis_queue))

        self.assertIsInstance(event, str)
        event_dict = json.loads(event)
        self.assertDictEqual(EXAMPLE_EVENT, event_dict)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
