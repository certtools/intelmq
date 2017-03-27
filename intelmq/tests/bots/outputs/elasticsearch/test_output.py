# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
import elasticsearch
from intelmq.bots.outputs.elasticsearch.output import ElasticsearchOutputBot

INPUT1 = {"__type": "Event",
          "classification.type": "botnet drone",
          "source.asn": 64496,
          "source.ip": "192.0.2.1",
          "feed.name": "Example Feed",
          "extra": '{"foo.bar": "test"}'
          }


@test.skip_database()
class TestElasticsearchOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ElasticsearchOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"flatten_fields": "extra"}
        cls.con = elasticsearch.Elasticsearch()

    def test_event(self):
        self.run_bot()
        result = self.con.search(index='intelmq')['hits']['hits'][0]
        self.assertDictEqual(result, {})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
