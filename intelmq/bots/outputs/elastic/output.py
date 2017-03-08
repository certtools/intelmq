# -*- coding: utf-8 -*-

import sys
from collections.abc import Mapping

from elasticsearch import Elasticsearch

from intelmq.lib.bot import Bot

#improved from https://stackoverflow.com/a/34615257
#still lacks recursion control check
#as noted in the comments

def replace_keys(obj, key_char = '.', replacement = '_'):
    if isinstance(obj, Mapping):
        return {key.replace('.', '_'): replace_keys(val,
                                                    replacement = replacement)
                    for key, val in obj.items()}
    return obj

class ElasticsearchOutputBot(Bot):

    def init(self):
        self.elastic_host = getattr(self.parameters,
                                    'elastic_host','127.0.0.1')
        self.elastic_port = getattr(self.parameters,
                                    'elastic_port','9200')
        self.elastic_index = getattr(self.parameters,
                                     'elastic_index', 'intelmq')
        self.elastic_doctype = getattr(self.parameters,
                                     'elastic_doctype', 'events')
        self.sanitize_keys = getattr(self.parameters,
                                     'sanitize_keys', True)
        self.replacement_char = getattr(self.parameters,
                                        'replacement_char', '_')
        self.es = Elasticsearch([
                    {'host': self.elastic_host, 'port': self.elastic_port}
                ])
        if not self.es.indices.exists(self.elastic_index):
            self.es.indices.create(index = self.elastic_index, ignore=400)

    def process(self):
        event = self.receive_message()
        event_dict = event.to_dict(hierarchical=False)
        if self.sanitize_keys:
            event_dict = replace_keys(event_dict,
                                      replacement = self.replacement_char)
        self.es.index(index = self.elastic_index,
                      doc_type = self.elastic_doctype,
                      body = event_dict)
        self.acknowledge_message()


BOT = ElasticsearchOutputBot
