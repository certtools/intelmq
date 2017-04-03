# -*- coding: utf-8 -*-
import time
import unittest

import elasticsearch

import intelmq.lib.test as test
from intelmq.bots.outputs.elasticsearch.output import ElasticsearchOutputBot

INPUT1 = {"__type": "Event",
          "classification.type": "botnet drone",
          "source.asn": 64496,
          "source.ip": "192.0.2.1",
          "feed.name": "Example Feed",
          "extra": '{"foo.bar": "test"}'
          }
OUTPUT1 = {'classification_type': 'botnet drone',
           'extra_foo_bar': 'test',
           'feed_name': 'Example Feed',
           'source_asn': 64496,
           'source_ip': '192.0.2.1',
           }
ES_SEARCH = {"query": {
    "constant_score": {
        "filter": {
            "term": {
                "source_asn": 64496
            }
        }
    }
}
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
        time.sleep(1)  # ES needs some time between inserting and searching
        result = self.con.search(index='intelmq', body=ES_SEARCH)['hits']['hits'][0]
        self.con.delete(index='intelmq', doc_type='events', id=result['_id'])
        self.assertDictEqual(OUTPUT1, result['_source'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
