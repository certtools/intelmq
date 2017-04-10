# -*- coding: utf-8 -*-
"""
The ES-connection can't be closed explicitly.
"""

from json import loads
from collections.abc import Mapping

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None

from intelmq.lib.bot import Bot


def replace_keys(obj, key_char='.', replacement='_'):
    if isinstance(obj, Mapping):
        replacement_obj = {}
        for key, val in obj.items():
            replacement_key = key.replace(key_char, replacement)
            replacement_obj[replacement_key] = replace_keys(val, key_char, replacement)
        return replacement_obj
    return obj


class ElasticsearchOutputBot(Bot):

    def init(self):
        if Elasticsearch is None:
            raise ValueError('Missing elasticsearch module.')

        self.elastic_host = getattr(self.parameters,
                                    'elastic_host', '127.0.0.1')
        self.elastic_port = getattr(self.parameters,
                                    'elastic_port', '9200')
        self.elastic_index = getattr(self.parameters,
                                     'elastic_index', 'intelmq')
        self.elastic_doctype = getattr(self.parameters,
                                       'elastic_doctype', 'events')
        self.replacement_char = getattr(self.parameters,
                                        'replacement_char', '_')
        self.flatten_fields = getattr(self.parameters,
                                      'flatten_fields', ['extra'])
        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')

        self.es = Elasticsearch([{'host': self.elastic_host,
                                  'port': self.elastic_port}])
        if not self.es.indices.exists(self.elastic_index):
            self.es.indices.create(index=self.elastic_index, ignore=400)

    def process(self):
        event = self.receive_message()
        event_dict = event.to_dict(hierarchical=False)

        for field in self.flatten_fields:
            if field in event_dict:
                val = event_dict[field]
                # if it's a string try to parse it as JSON
                if isinstance(val, str):
                    try:
                        val = loads(val)
                    except ValueError:
                        pass
                if isinstance(val, Mapping):
                    for key, value in val.items():
                        event_dict[field + '_' + key] = value
                    event_dict.pop(field)

        event_dict = replace_keys(event_dict,
                                  replacement=self.replacement_char)

        self.es.index(index=self.elastic_index,
                      doc_type=self.elastic_doctype,
                      body=event_dict)
        self.acknowledge_message()


BOT = ElasticsearchOutputBot
