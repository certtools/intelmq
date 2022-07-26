# SPDX-FileCopyrightText: 2020 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
    """Fetch data from the Apache Kafka distributed stream processing system"""
    bootstrap_servers: str = "localhost:9092"
    topic = []
    ssl_cafile = None
    ssl_certfile = None
    ssl_check_hostname = None

    def init(self):
        if kafka is None:
            raise MissingDependencyError("kafka")

        self.logger.debug(f"Topic set to {self.topic}, bootstrap_servers set to {self.bootstrap_servers}")
        self.logger.debug(f"ssl_cafile set to {self.ssl_cafile}, ssl_certfile set to {self.ssl_certfile}, ssl_check_hostname set to {self.ssl_check_hostname}")

    def process(self):
        " Fetch messages from the Kafka server and pass them on one by one "
        consumer = kafka.KafkaConsumer(self.topic, bootstrap_servers=self.bootstrap_servers, ssl_cafile=self.ssl_cafile, ssl_certfile=self.ssl_certfile, ssl_check_hostname=self.ssl_check_hostname, auto_offset_reset='earliest', consumer_timeout_ms=100, group_id=self._Bot__bot_id)
        for msg in consumer:
            consumer.commit()
            report = self.new_report()
            self.logger.debug(f"Received msg with offset {msg.offset} from kafka topic {msg.topic}: {msg.value.decode()}")
            if report.add('raw', msg.value.decode()):
                self.send_message(report)


BOT = KafkaCollectorBot
