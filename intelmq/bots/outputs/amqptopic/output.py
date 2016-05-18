# -*- coding: utf-8 -*-
import sys

from intelmq.lib.bot import Bot

import pika


class AMQPTopicBot(Bot):

    CONTENT_TYPE = 'application/json'
    DELIVERY_MODE = 1

    def init(self):
        self._connection = None
        self._channel = None
        self._exchange = self.parameters.exchange_name
        self._durable = bool(self.parameters.exchange_durable)
        self._type = self.parameters.exchange_type
        self._connection_host = self.parameters.connection_host
        self._connection_port = int(self.parameters.connection_port)
        self._connection_vhost = self.parameters.connection_vhost
        self._connection_attempts = int(self.parameters.connection_attempts)
        self._connection_heartbeat = int(self.parameters.connection_heartbeat)
        self._credentials = pika.PlainCredentials(self.parameters.username, self.parameters.password)
        self._connection_parameters = pika.ConnectionParameters(
                                          host=self._connection_host, 
                                          port=self._connection_port,
                                          virtual_host=self._connection_vhost, 
                                          connection_attempts=self._connection_attempts,
                                          heartbeat_interval=self._connection_heartbeat, 
                                          credentials=self._credentials)
        self._routing_key = self.parameters.routingkey
        self.connect_server()

    def connect_server(self):
        self.logger.info('AMQP Connecting to {}:{}/{} '.format(self._connection_host, self._connection_port, self._connection_vhost))
        try:
            self._connection = pika.BlockingConnection(self._connection_parameters)
        except:
            self.logger.exception(
                'AMQP connection to {}:{}/{} failled!!'.format(
                    self._connection_host,
                    self._connection_port,
                    self._connection_vhost))
        else:
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self._exchange, type=self._type, durable=self._durable)
            self._channel.confirm_delivery()

    def process(self):
        event = self.receive_message()

        # verify | set connection
        if None in (self._connection, self._channel):
            self.connect_server()

        properties = pika.BasicProperties(
            content_type=self.CONTENT_TYPE, delivery_mode=self.DELIVERY_MODE)

        try:
            if not self._channel.basic_publish(exchange=self._exchange,
                                               routing_key=self._routing_key,
                                               body=event.to_json(),
                                               properties=properties,
                                               mandatory=True):
                self.logger.error("Message sent but not confirmed")
        except Exception:
            self.logger.error("Error publishing the message")
        else:
            self.acknowledge_message()

if __name__ == "__main__":
    bot = AMQPTopicBot(sys.argv[1])
    bot.start()
