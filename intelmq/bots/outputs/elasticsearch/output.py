# -*- coding: utf-8 -*-
"""
The ES-connection can't be closed explicitly.
"""

from json import loads
from datetime import datetime
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
        self.rotate_index = getattr(self.parameters,
                                    'rotate_index', False)
        self.http_username = getattr(self.parameters,
                                     'http_username', None)
        self.http_password = getattr(self.parameters,
                                     'http_password', None)
        self.elastic_doctype = getattr(self.parameters,
                                       'elastic_doctype', 'events')
        self.replacement_char = getattr(self.parameters,
                                        'replacement_char', '_')
        self.flatten_fields = getattr(self.parameters,
                                      'flatten_fields', ['extra'])
        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')

        kwargs = {}
        if self.http_username and self.http_password:
            kwargs = {'http_auth': (self.http_username, self.http_password)}
        self.es = Elasticsearch([{'host': self.elastic_host, 'port': self.elastic_port}], **kwargs)

        if self.rotate_index:
            # Use time-based index names - check that the template exists
            if not self.es.indices.exists_template(name=self.elastic_index):
                print()  # error TODO

        else:
            # Using a single named index. Check that it exists
            if not self.es.indices.exists(self.elastic_index):
                self.es.indices.create(index=self.elastic_index, ignore=400)

    def get_index(self, event_dict):
        """
        Returns the correct index name to use for the given event,
         based on the current bot's settings and the event's date.
        :param event_dict: The event (as a dict) to examine.
        :return: A string containing the name of the index which should store the event.
        """
        # This function supports rotating indices based on timestamps.
        # If the bot should rotate indices, the index name will include a date stamp based on:
        #   - the time_source field - if one is available, else
        #   - the time_observation field - if one is available, else
        #   - the current time, if neither of the above is available.

        if self.rotate_index:
            event_date = None
            # Try to use the the time information from the event.
            for t in [event_dict.get('time_source', None), event_dict.get('time_observation', None)]:
                try:
                    event_date = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S+00:00').date()
                    # event_date = date.fromtimestamp(t)
                    break
                except (TypeError, ValueError) as e:
                    print("Error: {}".format(e))
                    event_date = None
                    continue

            # If no time available in the event, use today's date.
            event_date = event_date or datetime.today().date()

            print("Date: {}".format(event_date.isoformat()))
            return "{}-{}".format(self.elastic_index, event_date.isoformat())
        else:
            # If the bot should NOT rotate indices, just use the index name
            return self.elastic_index

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

        # TODO: Remove me
        # 2018-06-13T00:00:00+00:00
        # event_dict.update({"time_source": "2018-05-13T00:00:00+00:00"})

        self.es.index(index=self.get_index(event_dict),
                      doc_type=self.elastic_doctype,
                      body=event_dict)
        self.acknowledge_message()


BOT = ElasticsearchOutputBot
