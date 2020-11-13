"""
Kafka Collector Bot

Collects information from the Apache Kafka distributed stream processing system.

Args:
    topic (str): topic to collect information from
    bootstrap_servers (str): the ‘host[:port]’ string of the Apache Kafka system. Defaults to `localhost:9092`
"""

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import kafka
except ImportError:
    kafka = None


class KafkaCollectorBot(CollectorBot):

    def init(self):
        if kafka is None:
            raise MissingDependencyError("kafka")

        self.topic = []
        if getattr(self.parameters, 'topic', '') != '':
            self.topic = self.parameters.topic

        self.bootstrap_servers = 'localhost:9092'
        if getattr(self.parameters, 'bootstrap_servers', '') != '':
            self.bootstrap_servers = self.parameters.bootstrap_servers

        self.ssl_cafile = getattr(self.parameters, 'ssl_ca_certificate', None)
        self.ssl_certfile = getattr(self.parameters, 'ssl_client_certificate', None)
        self.ssl_check_hostname = getattr(self.parameters, 'ssl_check_hostname', False)

        self.logger.debug("Topic set to {}, bootstrap_servers set to {}".format(self.topic, self.bootstrap_servers))
        self.logger.debug("ssl_cafile set to {}, ssl_certfile set to {}, ssl_check_hostname set to {}".format(self.ssl_cafile, self.ssl_certfile, self.ssl_check_hostname))

    def process(self):
        " Fetch messages from the Kafka server and pass them on one by one "
        consumer = kafka.KafkaConsumer(self.topic, bootstrap_servers=self.bootstrap_servers, ssl_cafile=self.ssl_cafile, ssl_certfile=self.ssl_certfile, ssl_check_hostname=self.ssl_check_hostname, auto_offset_reset='earliest', consumer_timeout_ms=100, group_id=self._Bot__bot_id)
        for msg in consumer:
            consumer.commit()
            report = self.new_report()
            self.logger.debug("Received msg with offset {} from kafka topic {}: {}".format(msg.offset, msg.topic, msg.value.decode()))
            if report.add('raw', msg.value.decode()):
                self.send_message(report)


BOT = KafkaCollectorBot
