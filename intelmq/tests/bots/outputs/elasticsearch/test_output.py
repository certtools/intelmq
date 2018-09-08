# -*- coding: utf-8 -*-
import os
import time
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.elasticsearch.output import ElasticsearchOutputBot

if os.environ.get('INTELMQ_TEST_DATABASES'):
    import elasticsearch


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
        if os.environ.get('INTELMQ_TEST_DATABASES'):
            cls.con = elasticsearch.Elasticsearch()

    def test_event(self):
        self.run_bot()
        time.sleep(1)  # ES needs some time between inserting and searching
        result = self.con.search(index='intelmq', body=ES_SEARCH)['hits']['hits'][0]
        self.con.delete(index='intelmq', doc_type='events', id=result['_id'])
        self.assertDictEqual(OUTPUT1, result['_source'])


TIMESTAMP_1 = "1869-12-02T00:00:00+00:00"
TIMESTAMP_2 = "2020-02-02T01:23:45+00:00"


class TestElasticsearchRotatingIndices(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ElasticsearchOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"flatten_fields": "extra",
                         "elastic_index": "intelmq",
                         "elastic_doctype": "events",
                         "rotate_index": "true"}
        if os.environ.get('INTELMQ_TEST_DATABASES'):
            cls.con = elasticsearch.Elasticsearch()

    def test_index_detected_from_time_source(self):
        # Use the sample input, but set the source timestamp
        self.input_message = INPUT1.update({"time_source": TIMESTAMP_1})
        expected_index_name = "{}-1869-12-02".format(self.sysconfig.get('elastic_index'))

        self.run_bot()
        time.sleep(1)  # Let ES store the event. Can also force this with ES API

        result = self.con.search(index=self.sysconfig.get('elastic_index'), body=ES_SEARCH)['hits']['hits'][0]
        result_index_name = result["_index"]

        # Clean up test event and check that the index name was set correctly
        self.con.delete(index=result_index_name, doc_type=self.sysconfig.get('doc_type'), id=result['_id'])
        self.assertEqual(result_index_name, expected_index_name)

    def test_index_detected_from_time_observation(self):
        # Use the sample input, but set the observation timestamp
        self.input_message = INPUT1.update({"time_observation": TIMESTAMP_2})
        expected_index_name = "{}-2020-02-02".format(self.sysconfig.get('elastic_index'))

        self.run_bot()
        time.sleep(1)  # Let ES store the event. Can also force this with ES API

        result = self.con.search(index=self.sysconfig.get('elastic_index'), body=ES_SEARCH)['hits']['hits'][0]
        result_index_name = result["_index"]

        # Clean up test event and check that the index name was set correctly
        self.con.delete(index=result_index_name, doc_type=self.sysconfig.get('doc_type'), id=result['_id'])
        self.assertEqual(result_index_name, expected_index_name)

    # def test_index_detected_current_date(self):
    #     self.input_message = INPUT1.update({})  # TODO: Mock datetime object


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
