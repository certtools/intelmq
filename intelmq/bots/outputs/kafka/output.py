# -*- coding: utf-8 -*-

from json import loads
from json import dumps
from json import load
from collections.abc import Mapping

try:
    from confluent_kafka import Producer
except ImportError:
    Producer = None
try:
    from confluent_kafka import avro
except ImportError:
    avro = None

if avro is not None:
    from confluent_kafka.avro import AvroProducer

from intelmq.lib.bot import Bot
from intelmq.lib.utils import load_configuration

def replace_keys(obj, key_char='.', replacement='_'):
    if isinstance(obj, Mapping):
        replacement_obj = {}
        for key, val in obj.items():
            replacement_key = key.replace(key_char, replacement)
            replacement_obj[replacement_key] = replace_keys(val, key_char, replacement)
        return replacement_obj
    return obj

class KafkaOutputBot(Bot):

    def init(self):
        if Producer is None:
            raise ValueError('Missing confluent-kafka-python module.')
        if avro is None:
            raise ValueError('Missing python3-avro module')

        self.broker_list = getattr(
            self.parameters, 'kafka_broker_list', '127.0.0.1:9092')
        self.kafka_topic = getattr(
            self.parameters, 'kafka_topic', 'intelmq')
        self.flatten_fields = getattr(
            self.parameters, 'flatten_fields', ['extra'])
        self.enable_avro = getattr(
            self.parameters, 'enable_avro', False)

        # Fields below are to define an output schema via AVRO
        if self.enable_avro is True:

            self.avro_value_schema = avro.loads(
                dumps(load_configuration(self.parameters.avro_value_schema_file)))
            self.avro_key_schema = avro.loads(
                dumps(load_configuration(self.parameters.avro_key_schema_file)))

            self.avro_topic_schema = load_configuration(self.parameters.avro_topic_schema)

            self.avro_topic_field = getattr(
                self.parameters, 'avro_topic_field', None)
            self.avro_schema_registry = getattr(
                self.parameters, 'avro_schema_registry', None)
            
            # Build a list of producers for each destination topic 
            self.producer = AvroProducer(
                    {
                        'bootstrap.servers': self.broker_list,
                        'schema.registry.url': self.avro_schema_registry
                    },
                    default_key_schema=self.avro_key_schema,
                    default_value_schema = self.avro_value_schema)
        else:
            self.producer = Producer(
                    {
                        'bootstrap.servers': self.broker_list
                    })


        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')


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
                        event_dict[field + '.' + key] = value
                    event_dict.pop(field)

        event_dict = replace_keys(event_dict)

        if self.enable_avro is False:
            self.producer.produce(self.kafka_topic, dumps(event_dict).encode('utf-8'), callback=self.delivery_report)
            self.acknowledge_message()
            self.kafka.flush()
        else:
            try:
                key_field = str(event_dict[self.avro_topic_field]).replace('.','_')
            except KeyError:
                self.logger.debug('Event %s has no field %s, dropping.', format(event_dict),format(self.avro_topic_field))
                self.acknowledge_message()
                return
                
            submit_key =  {'indicator':event_dict[key_field]}
            event_topic = self.avro_topic_schema[key_field]
            self.logger.debug('Shipped %s to topic: %s', format(submit_key),format(event_topic))
            self.producer.produce(topic=event_topic, value=event_dict, key=submit_key)
            self.acknowledge_message()
            self.producer.poll(0)

    def delivery_report(self, err, msg):
        """ Called once for each message produced to flag for failure.
        Triggered by poll() or flush()."""
        if err is not None:
            self.logger.exception('Message delivery failed: {}'.format(err))


BOT = KafkaOutputBot
