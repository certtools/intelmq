# -*- coding: utf-8 -*-
import os
import time
import unittest
import unittest.mock as mock
from datetime import datetime

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
SAMPLE_TEMPLATE = {
    "mappings": {
        "events": {
            "properties": {
                "time_observation": {
                    "type": "date"
                },
                "time_source": {
                    "type": "date"
                },
                "classification_type": {
                    "type": "keyword"
                },
                "source_asn": {
                    "type": "integer"
                },
                "feed_name": {
                    "type": "text"
                },
                "source_ip": {
                    "type": "ip"
                }
            }
        }
    },
    "template": "intelmq-*",
    "index_patterns": [
        "intelmq-*"
    ]
}

TIMESTAMP_1 = "1869-12-02T00:00:00+00:00"
TIMESTAMP_2 = "2020-02-02T01:23:45+00:00"
TIMESTAMP_3 = "2018-09-09T01:23:45+00:00"
INPUT_TIME_SOURCE = {
    "__type": "Event",
    "classification.type": "botnet drone",
    "source.asn": 64496,
    "source.ip": "192.0.2.1",
    "feed.name": "Example Feed",
    "time.source": TIMESTAMP_1,
    "extra": '{"foo.bar": "test"}'
}
INPUT_TIME_OBSERVATION = {
    "__type": "Event",
    "classification.type": "botnet drone",
    "source.asn": 64496,
    "source.ip": "192.0.2.1",
    "feed.name": "Example Feed",
    "time.observation": TIMESTAMP_2,
    "extra": '{"foo.bar": "test"}'
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

    def test_raise_when_no_template(self):
        """
        Test that a bot raises a RuntimeError if 'rotate_index' is set, but a matching template doesn't exist in ES.
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "elastic_doctype": "events",
                          "rotate_index": "true"}
        self.assertRaises(RuntimeError, self.run_bot())

    def test_index_detected_from_time_source(self):
        """
        Tests whether an input event with a time.source field is indexed according to its time.source date.
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "elastic_doctype": "events",
                          "rotate_index": "true"}
        expected_index_name = "{}-1869-12-02".format(self.sysconfig.get('elastic_index'))
        self.base_check_expected_index_created(INPUT_TIME_SOURCE, expected_index_name)

    def test_index_detected_from_time_observation(self):
        """
        Tests whether an input event with a time.observation field (and no time.source field) is indexed according to
        its time.observation date.
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "elastic_doctype": "events",
                          "rotate_index": "true"}
        expected_index_name = "{}-2020-02-02".format(self.sysconfig.get('elastic_index'))
        self.base_check_expected_index_created(INPUT_TIME_OBSERVATION, expected_index_name)

    def test_default_index_created(self):
        """
        Tests whether an event with no time information is indexed using the default value
        :return:
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "elastic_doctype": "events",
                          "rotate_index": "true"}

        expected_index_name = "{}-unknown-date".format(self.sysconfig.get('elastic_index'))
        self.base_check_expected_index_created(INPUT1, expected_index_name)

    def test_index_falls_back_to_default(self):
        """
        Tests whether get_index returns an expected default value
         if no time.source or time.observation is present.
        """

        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "elastic_doctype": "events",
                          "rotate_index": "true"}

        self.prepare_bot()
        index = self.bot.get_index(INPUT1, 'test-default')

        self.assertEqual(index, 'intelmq-test-default')

    def base_check_expected_index_created(self, input_event, expected_index_name):
        self.input_message = input_event

        self.assertFalse(self.con.indices.exists(expected_index_name))  # Index should not already exist

        # Create the template mapping in Elasticsearch
        self.con.indices.put_template(name=self.sysconfig.get('elastic_index'), body=SAMPLE_TEMPLATE)

        self.run_bot()
        time.sleep(1)  # Let ES store the event. Can also force this with ES API

        self.assertTrue(self.con.indices.exists(expected_index_name))

        result = self.con.search(index=expected_index_name, body=ES_SEARCH)['hits']['hits'][0]
        result_index_name = result["_index"]

        # Clean up test event and check that the index name was set correctly
        self.con.delete(index=result_index_name, doc_type=self.sysconfig.get('elastic_doctype'), id=result['_id'])
        self.assertEqual(result_index_name, expected_index_name)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
