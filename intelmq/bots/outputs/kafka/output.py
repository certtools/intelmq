# -*- coding: utf-8 -*-

from json import loads
from json import dumps
from collections.abc import Mapping

try:
    from confluent_kafka import Producer
except ImportError:
    Producer = None

from intelmq.lib.bot import Bot

class KafkaOutputBot(Bot):

    def init(self):
        if Producer is None:
            raise ValueError('Missing confluent-kafka-python module.')

        self.broker_list = getattr(self.parameters,
                                    'kafka_broker_list', '127.0.0.1:9092')
        self.kafka_topic = getattr(self.parameters,
                                    'kafka_topic', 'intelmq')
        self.flatten_fields = getattr(self.parameters,
                                    'flatten_fields', ['extra'])
        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')

        self.kafka = Producer({'bootstrap.servers': self.broker_list})

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

        self.kafka.produce(self.kafka_topic, dumps(event_dict).encode('utf-8'), callback=self.delivery_report)
        self.acknowledge_message()
        self.kafka.flush()

    def delivery_report(self, err, msg):
        """ Called once for each message produced to flag for failure.
        Triggered by poll() or flush()."""
        if err is not None:
            self.logger.exception('Message delivery failed: {}'.format(err))

BOT = KafkaOutputBot
