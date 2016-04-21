# -*- coding: utf-8 -*-

import json
import unittest
from pprint import pprint

import intelmq.lib.test as test
import intelmq.lib.utils as utils
import redis
from intelmq.bots.outputs.redis.output import RedisOutputBot

EXAMPLE_EVENT  = {"classification.type": "malware",
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
                  "source.port": 65118, "__type": "Event",
                  "feed.name": "BitSight",
                  "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTYWxpdHlwMnAiLCJlbnYiOnsic"
                  "mVtb3RlX2FkZHIiOiIxNTIuMTY2LjExOS4yIiwicmVtb3RlX3"
                  "BvcnQiOiI2NTExOCIsInNlcnZlcl9hZGRyIjoiNTIuMTguMTk"
                  "2LjE2OSIsInNlcnZlcl9wb3J0IjoiOTc5NiJ9LCJfdHMiOjE0"
                  "NjExMDc3NjgsIl9nZW9fZW52X3JlbW90ZV9hZGRyIjp7ImNvd"
                  "W50cnlfbmFtZSI6IkRvbWluaWNhbiBSZXB1YmxpYyJ9fQ=="
                  }

EXAMPLE_OUTPUT  = {"classification": {"type": "malware"},
                   "feed": {"url": "http://alerts.bitsighttech.com:8080/stream?",
                            "name": "BitSight", "accuracy": 100.0},
                   "source": {"port": 65118, "ip": "152.166.119.2",
                              "geolocation": {"country": "Dominican Republic"}},
                   "malware": {"name": "salityp2p"},
                   "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTYWxpdHlwMnAiLCJlbnYiOnsicmVtb3"
                   "RlX2FkZHIiOiIxNTIuMTY2LjExOS4yIiwicmVtb3RlX3BvcnQiOiI2NTExOCI"
                   "sInNlcnZlcl9hZGRyIjoiNTIuMTguMTk2LjE2OSIsInNlcnZlcl9wb3J0Ijoi"
                   "OTc5NiJ9LCJfdHMiOjE0NjExMDc3NjgsIl9nZW9fZW52X3JlbW90ZV9hZGRyI"
                   "jp7ImNvdW50cnlfbmFtZSI6IkRvbWluaWNhbiBSZXB1YmxpYyJ9fQ==",
                   "destination": {"port": 9796, "ip": "52.18.196.169"},
                   "event_description": {"text": "Sinkhole attempted connection"},
                   "time": {"source": "2016-04-19T23:16:08+00:00",
                            "observation": "2016-04-19T23:16:08+00:00"}
                   }


class TestRedisOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RedisOutputBot
        cls.default_input_message = EXAMPLE_EVENT

    def test_event(self):
        """ test output """
        self.host = test.BOT_CONFIG['redis_server_ip']
        self.port = test.BOT_CONFIG['redis_server_port']
        self.db = test.BOT_CONFIG['redis_db']
        self.queue = test.BOT_CONFIG['redis_queue']
        self.password = test.BOT_CONFIG['redis_password']
        self.timeout = test.BOT_CONFIG['redis_timeout']
        self.conn = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)

        self.output = redis.StrictRedis(connection_pool=self.conn, socket_timeout=self.timeout, password=self.password)
        self.run_bot()
        OUTPUT = self.output.lpop(self.queue)
        event = utils.decode(OUTPUT)

        self.assertIsInstance(event, str)
        event_dict = json.loads(event)
        del event_dict['time']['observation']
        del EXAMPLE_OUTPUT['time']['observation']

        self.assertDictEqual(EXAMPLE_OUTPUT, event_dict)


if __name__ == '__main__':
    unittest.main()
