# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.mongodb.output import MongoDBOutputBot

if os.environ.get('INTELMQ_TEST_DATABASES'):
    import pymongo

INPUT1 = {"__type": "Event",
          "classification.type": "botnet drone",
          "source.asn": 64496,
          "source.ip": "192.0.2.1",
          "feed.name": "Example Feed",
          "extra": '{"foo.bar": "test"}'
          }
OUTPUT1 = {'classification': {'type': 'botnet drone'},
           'extra': '{"foo.bar": "test"}',
           'feed': {'name': 'Example Feed'},
           'source': {'asn': 64496, 'ip': '192.0.2.1'},
           }


@test.skip_database()
class TestMongoDBOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MongoDBOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"collection": "events",
                         "database": "tests",
                         "host": "localhost",
                         "port": 27017,
                         "hierarchical_output": True}
        if not os.environ.get('INTELMQ_TEST_DATABASES'):
            return
        cls.con = pymongo.MongoClient()
        cls.db = cls.con['tests']

    def test_event(self):
        self.run_bot()
        result = self.db['events'].find_one_and_delete({"source.asn": 64496})
        del result['_id']
        self.assertDictEqual(OUTPUT1, result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
