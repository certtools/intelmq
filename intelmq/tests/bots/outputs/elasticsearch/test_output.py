# -*- coding: utf-8 -*-
import os
import unittest
import unittest.mock as mock
from datetime import datetime

import intelmq.lib.test as test
from intelmq.bots.outputs.elasticsearch.output import ElasticsearchOutputBot, get_event_date

if os.environ.get('INTELMQ_TEST_DATABASES'):
    import elasticsearch

INPUT1 = {
    "__type": "Event",
    "classification.type": "infected-system",
    "source.asn": 64496,
    "source.ip": "192.0.2.1",
    "feed.name": "Example Feed",
    "extra": '{"foo.bar": "test"}'
}
OUTPUT1 = {
    'classification.type': 'infected-system',
    'extra.foo.bar': 'test',
    'feed.name': 'Example Feed',
    'source.asn': 64496,
    'source.ip': '192.0.2.1',
}
OUTPUT1_REPLACEMENT_CHARS = {
    'classification_type': 'infected-system',
    'extra_foo_bar': 'test',
    'feed_name': 'Example Feed',
    'source_asn': 64496,
    'source_ip': '192.0.2.1',
}
ES_SEARCH = {
    "query": {
        "constant_score": {
            "filter": {
                "term": {
                    "source.asn": 64496
                }
            }
        }
    }
}
ES_SEARCH_REPLACEMENT_CHARS = {
    "query": {
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
        "properties": {
            "time.observation": {
                "type": "date"
            },
            "time.source": {
                "type": "date"
            },
            "classification.type": {
                "type": "keyword"
            },
            "source.asn": {
                "type": "integer"
            },
            "feed.name": {
                "type": "text"
            },
            "source.ip": {
                "type": "ip"
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
    "classification.type": "infected-system",
    "source.asn": 64496,
    "source.ip": "192.0.2.1",
    "feed.name": "Example Feed",
    "time.source": TIMESTAMP_1,
    "extra": '{"foo.bar": "test"}'
}
INPUT_TIME_OBSERVATION = {
    "__type": "Event",
    "classification.type": "infected-system",
    "source.asn": 64496,
    "source.ip": "192.0.2.1",
    "feed.name": "Example Feed",
    "time.observation": TIMESTAMP_2,
    "extra": '{"foo.bar": "test"}'
}

ROTATE_OPTIONS = {
    'never': None,
    'daily': '%Y-%m-%d',
    'weekly': '%Y-%W',
    'monthly': '%Y-%m',
    'yearly': '%Y'
}


@test.skip_database()
class TestElasticsearchOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ElasticsearchOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"flatten_fields": "extra",
                         "rotate_index": "never"}
        if os.environ.get('INTELMQ_TEST_DATABASES'):
            cls.con = elasticsearch.Elasticsearch()

    def test_event(self):
        self.run_bot()
        self.con.indices.refresh(index="intelmq")  # Make Elasticsearch propagate the new document
        result = self.con.search(index='intelmq', body=ES_SEARCH)['hits']['hits'][0]
        self.con.delete(index='intelmq',
                        id=result['_id'])
        self.assertDictEqual(OUTPUT1, result['_source'])

    def test_get_event_date(self):
        """
        Test whether get_event_date detects the time.source and time.observation fields in an event.
        """
        self.assertEqual(get_event_date(INPUT_TIME_SOURCE),
                         datetime.strptime(TIMESTAMP_1, '%Y-%m-%dT%H:%M:%S+00:00').date())
        self.assertEqual(get_event_date(INPUT_TIME_OBSERVATION),
                         datetime.strptime(TIMESTAMP_2, '%Y-%m-%dT%H:%M:%S+00:00').date())

    def test_replacement_characters(self):
        """
        Checks that dots in field names are replaced with the replacement character if one is set.
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "replacement_char": "_",
                          "rotate_index": "never"}
        self.run_bot()
        self.con.indices.refresh(index="intelmq")  # Make Elasticsearch propagate the new document
        result = self.con.search(index=self.sysconfig.get('elastic_index'),
                                 body=ES_SEARCH_REPLACEMENT_CHARS)['hits']['hits'][0]

        self.con.delete(index=self.sysconfig.get('elastic_index'),
                        id=result['_id'])

        self.assertDictEqual(OUTPUT1_REPLACEMENT_CHARS, result['_source'])

    def test_index_detected_from_time_source(self):
        """
        Tests whether an input event with a time.source field is indexed according to its time.source date.
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "rotate_index": "daily"}
        expected_index_name = "{}-1869-12-02".format(self.sysconfig.get('elastic_index'))
        self.base_check_expected_index_created(INPUT_TIME_SOURCE, expected_index_name)

    def test_index_detected_from_time_observation(self):
        """
        Tests whether an input event with a time.observation field (and no time.source field) is indexed according to
        its time.observation date.
        """
        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "rotate_index": "daily"}
        expected_index_name = "{}-2020-02-02".format(self.sysconfig.get('elastic_index'))
        self.base_check_expected_index_created(INPUT_TIME_OBSERVATION, expected_index_name)

    def test_index_falls_back_to_default_date(self):
        """
        Tests whether get_index returns an expected default date
         if no time.source or time.observation is present, and
         that the OutputBot will use the current date if none is present.
        """

        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "rotate_index": "daily"}

        class FakeDateTime(datetime):
            """
            Passed to bot to force expected datetime value for test.
            """

            @classmethod
            def today(cls):
                return datetime.strptime('2018-09-09T01:23:45+00:00', '%Y-%m-%dT%H:%M:%S+00:00')

        expected_index_name = "{}-{}".format(self.sysconfig.get('elastic_index'), "2018-09-09")

        # Patch datetime with FakeDateTime, run the bot, and check the created index.
        with mock.patch('intelmq.bots.outputs.elasticsearch.output.datetime', new=FakeDateTime):
            self.base_check_expected_index_created(INPUT1, expected_index_name)

    def test_index_falls_back_to_default_string(self):
        """
        Tests whether get_index returns an expected default string
         if no time.source or time.observation is present, and
         that the OutputBot will use the current date if none is present.
        """

        self.sysconfig = {"flatten_fields": "extra",
                          "elastic_index": "intelmq",
                          "rotate_index": "daily"}

        self.prepare_bot()
        index = self.bot.get_index(INPUT1, default_string='test-default')
        self.assertEqual(index, 'intelmq-test-default')  # Check that get_index honors the supplied default string
        self.run_bot()  # Run to clear output queue. Will still index according to current date.

    def base_check_expected_index_created(self, input_event, expected_index_name):
        self.input_message = input_event

        self.assertFalse(self.con.indices.exists(expected_index_name))  # Index should not already exist

        # Create the template mapping in Elasticsearch
        self.con.indices.put_template(name=self.sysconfig.get('elastic_index'), body=SAMPLE_TEMPLATE)

        self.run_bot()
        self.con.indices.refresh(index=expected_index_name)  # Make Elasticsearch propagate the new document

        self.assertTrue(self.con.indices.exists(expected_index_name))

        result = self.con.search(index=expected_index_name, body=ES_SEARCH)['hits']['hits'][0]
        result_index_name = result["_index"]

        # Clean up test event and check that the index name was set correctly
        self.con.delete(index=result_index_name,
                        id=result['_id'])
        self.assertEqual(result_index_name, expected_index_name)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
