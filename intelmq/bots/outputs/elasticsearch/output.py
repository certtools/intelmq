# -*- coding: utf-8 -*-
"""
The ES-connection can't be closed explicitly.

TODO:
    * Support client_cert and client_key parameters, see https://github.com/certtools/intelmq/pull/1406
"""

from collections.abc import Mapping
from datetime import datetime
from json import loads

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None


ROTATE_OPTIONS = {
    'never': None,
    'daily': '%Y-%m-%d',
    'weekly': '%Y-%W',
    'monthly': '%Y-%m',
    'yearly': '%Y'
}


def replace_keys(obj, key_char='.', replacement='_'):
    if isinstance(obj, Mapping):
        replacement_obj = {}
        for key, val in obj.items():
            replacement_key = key.replace(key_char, replacement)
            replacement_obj[replacement_key] = replace_keys(val, key_char, replacement)
        return replacement_obj
    return obj


def get_event_date(event_dict: dict) -> datetime.date:
    event_date = None
    for t in [event_dict.get('time.source', None), event_dict.get('time.observation', None)]:
        try:
            event_date = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S+00:00').date()
            break
        except (TypeError, ValueError):
            # Ignore missing or invalid time_source or time_observation
            event_date = None
            continue
    return event_date


class ElasticsearchOutputBot(Bot):

    def init(self):
        if Elasticsearch is None:
            raise MissingDependencyError('elasticsearch', version='>=5.0.0,<6.0.0')

        self.elastic_host = getattr(self.parameters,
                                    'elastic_host', '127.0.0.1')
        self.elastic_port = getattr(self.parameters,
                                    'elastic_port', '9200')
        self.elastic_index = getattr(self.parameters,
                                     'elastic_index', 'intelmq')
        self.rotate_index = getattr(self.parameters,
                                    'rotate_index', False)
        self.use_ssl = getattr(self.parameters,
                               'use_ssl', False)
        self.ssl_ca_certificate = getattr(self.parameters,
                                          'ssl_ca_certificate', None)
        self.ssl_show_warnings = getattr(self.parameters,
                                         'ssl_show_warnings', True)
        self.replacement_char = getattr(self.parameters,
                                        'replacement_char', None)
        self.flatten_fields = getattr(self.parameters,
                                      'flatten_fields', ['extra'])
        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')

        self.set_request_parameters()  # Not all parameters set here are used by the ES client

        self.es = Elasticsearch([{'host': self.elastic_host, 'port': self.elastic_port}],
                                http_auth=self.auth,
                                use_ssl=self.use_ssl,
                                verify_certs=self.http_verify_cert,
                                ca_certs=self.ssl_ca_certificate,
                                ssl_show_warn=self.ssl_show_warnings,
                                )

        if self.should_rotate():
            # Use rotating index names - check that the template exists
            if not self.es.indices.exists_template(name=self.elastic_index):
                raise RuntimeError("No template with the name '{}' exists on the Elasticsearch host, "
                                   "but 'rotate_index' is set. "
                                   "Have you created the template?".format(self.elastic_index))

        else:
            # Using a single named index. Check that it exists and create it if it doesn't
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

        # For ES 2.x, replace dots with a specified replacement character
        if self.replacement_char and self.replacement_char != '.':
            event_dict = replace_keys(event_dict,
                                      replacement=self.replacement_char)

        self.es.index(index=self.get_index(event_dict, default_date=datetime.today().date()),
                      body=event_dict)
        self.acknowledge_message()

    def should_rotate(self):
        return self.rotate_index and ROTATE_OPTIONS.get(self.rotate_index)

    def get_index(self, event_dict: dict, default_date: datetime.date = None,
                  default_string: str = "unknown-date") -> str:
        """
        Returns the index name to use for the given event,
         based on the current bot's settings and the event's date fields.
         - If the bot should rotate its Elasticsearch index, returns elastic_index-<timestamp>
         based on the bot's rotation option and the time fields in the event, e.g. intelmq-2018.
         - If the bot should rotate its Elasticsearch index, but no time information is available in the event,
         this will return <elastic_index>-<default>, e.g. intelmq-unknown-date.
         - If the bot should not rotate indices, returns elastic_index, e.g. intelmq.

        :param event_dict: The event (as a dict) to examine.
        :param default_date: (Optional) The default date to use for events with no time information
          (e.g. datetime.today()). Default: None.
        :param default_string: (Optional) The value to append if no time is available in the event.
          Default: 'unknown-date'.
        :return: A string containing the name of the index which should store the event.
        """
        # This function supports rotating indices based on event timestamps.
        # If the bot should rotate indices, the index name will include a date stamp based on:
        #   - the time_source field - if one is available, else
        #   - the time_observation field - if one is available, else
        #   - the string given in the 'default' parameter, if neither date field is available

        if self.should_rotate():

            # Extract date information from the event. If none is present, use the default_date parameter.
            event_date = get_event_date(event_dict) or default_date

            # If no time available in the event and no default date is given, use the default catchall string
            event_date = event_date.strftime(ROTATE_OPTIONS.get(self.rotate_index)) if event_date else default_string
            return "{}-{}".format(self.elastic_index, event_date)
        else:
            # If the bot should NOT rotate indices, just use the index name
            return self.elastic_index


BOT = ElasticsearchOutputBot
