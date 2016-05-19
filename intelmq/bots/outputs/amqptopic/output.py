# -*- coding: utf-8 -*-
import sys

import pika
from intelmq.lib.bot import Bot


class AMQPTopicBot(Bot):

    def init(self):
        self.connection = None
        self.channel = None
        self.keep_raw_field = bool(self.parameters.keep_raw_field)
        self.delivery_mode = int(self.parameters.delivery_mode)
        self.content_type = self.parameters.content_type
        self.exchange = self.parameters.exchange_name
        self.require_confirmation = bool(self.parameters.require_confirmation)
        self.durable = bool(self.parameters.exchange_durable)
        self.exchange_type = self.parameters.exchange_type
        self.connection_host = self.parameters.connection_host
        self.connection_port = int(self.parameters.connection_port)
        self.connection_vhost = self.parameters.connection_vhost
        self.connection_attempts = int(self.parameters.connection_attempts)
        self.connection_heartbeat = int(self.parameters.connection_heartbeat)
        self.credentials = pika.PlainCredentials(self.parameters.username, self.parameters.password)
        self.connection_parameters = pika.ConnectionParameters(
            host=self.connection_host,
            port=self.connection_port,
            virtual_host=self.connection_vhost,
            connection_attempts=self.connection_attempts,
            heartbeat_interval=self.connection_heartbeat,
            credentials=self.credentials)
        self.routing_key = self.parameters.routing_key
        self.properties = pika.BasicProperties(
            content_type=self.content_type, delivery_mode=self.delivery_mode)
        self.connect_server()

    def connect_server(self):
        self.logger.info('AMQP Connecting to {}:{}/{} '.format(self.connection_host,
                                                               self.connection_port, self.connection_vhost))
        try:
            self.connection = pika.BlockingConnection(self.connection_parameters)
        except pika.exceptions.AMQPConnectionError:
            self.logger.exception(
                'AMQP connection to {}:{}/{} failled!!'.format(
                    self.connection_host,
                    self.connection_port,
                    self.connection_vhost))
        else:
            self.logger.info('AMQP Connected!! to {}:{}/{} '.format(self.connection_host,
                                                                    self.connection_port, self.connection_vhost))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, type=self.exchange_type, durable=self.durable)
            self.channel.confirm_delivery()

    def process(self):
        ''' Stop the Bot if cannot connect to AMQP Server after the defined connection attempts '''

        try:
            if (self.connection.is_closed or self.channel.is_closed):
                self.connect_server()
        except AttributeError:
            self.logger.exception('Bad configuration or server unavailable! Exiting...')
            self.stop()

        event = self.receive_message()

        if (not self.keep_raw_field):
            del event['raw']

        ''' If routing key or exchange name are invalid or non existent, the message is accepted by the server but we receive no confirmation '''
        ''' Allways require confirmation. If parameter require_confirmation is True and no confirmation is received, raise error. '''

        try:
            if not self.channel.basic_publish(exchange=self.exchange,
                                              routing_key=self.routing_key,
                                              body=event.to_json(),
                                              properties=self.properties,
                                              mandatory=True):
                self.logger.error("Message sent but not confirmed")
                if self.require_confirmation:
                    raise NameError('Message sent but not confirmed')
        except (pika.exceptions.ChannelError, pika.exceptions.AMQPChannelError, pika.exceptions.NackError):
            self.logger.exception("Error publishing the message")
        else:
            self.acknowledge_message()

if __name__ == "__main__":
    bot = AMQPTopicBot(sys.argv[1])
    bot.start()
