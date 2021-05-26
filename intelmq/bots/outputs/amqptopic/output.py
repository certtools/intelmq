# SPDX-FileCopyrightText: 2016 Pedro Reis
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import ssl

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pika
except ImportError:
    pika = None


class AMQPTopicOutputBot(OutputBot):
    """Send events to an AMQP topic exchange. Requires the pika python library"""
    connection_attempts: int = 3
    connection_heartbeat: int = 3600
    connection_host: str = "127.0.0.1"  # TODO: could be ipaddress
    connection_port: int = 5672
    connection_vhost: str = None
    content_type: str = "application/json"
    delivery_mode: int = 2
    exchange_durable: bool = True
    exchange_name: str = None
    format_routing_key: bool = False
    exchange_type: str = "topic"
    keep_raw_field: bool = False  # TODO: legacy? not used..
    message_hierarchical_output: bool = False
    message_jsondict_as_string: bool = False
    message_with_type: bool = False
    password: str = None
    require_confirmation: bool = True
    routing_key: str = None
    single_key: bool = False
    use_ssl = False
    username = None

    _connection = None

    def init(self):
        if pika is None:
            raise MissingDependencyError("pika")

        self._connection = None
        self.channel = None

        pika_version = tuple(int(x) for x in pika.__version__.split('.'))
        self.kwargs = {}
        if pika_version < (0, 11):
            self.kwargs['heartbeat_interval'] = self.connection_heartbeat
        else:
            self.kwargs['heartbeat'] = self.connection_heartbeat
        if pika_version < (1, ):
            # https://groups.google.com/forum/#!topic/pika-python/gz7lZtPRq4Q
            self.publish_raises_nack = False
        else:
            self.publish_raises_nack = True

        if self.username is not None and self.password is not None:
            self.kwargs['credentials'] = pika.PlainCredentials(self.username,
                                                               self.password)

        if self.use_ssl:
            self.kwargs['ssl_options'] = pika.SSLOptions(context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))

        self.connection_parameters = pika.ConnectionParameters(
            host=self.connection_host,
            port=self.connection_port,
            virtual_host=self.connection_vhost,
            connection_attempts=self.connection_attempts,
            **self.kwargs)
        self.routing_key = self.routing_key
        self.properties = pika.BasicProperties(
            content_type=self.content_type, delivery_mode=self.delivery_mode)

        self.connect_server()

    def connect_server(self):
        self.logger.info('AMQP Connecting to %s:%s/%s.',
                         self.connection_host, self.connection_port, self.connection_vhost)
        try:
            self._connection = pika.BlockingConnection(self.connection_parameters)
        except pika.exceptions.ProbableAuthenticationError:
            self.logger.error('AMQP authentication failed!')
            raise
        except pika.exceptions.ProbableAccessDeniedError:
            self.logger.error('AMQP authentication for virtual host failed!')
            raise
        except pika.exceptions.AMQPConnectionError:
            self.logger.error('AMQP connection failed!')
            raise
        else:
            self.logger.info('AMQP connection successful.')
            self.channel = self._connection.channel()
            if self.exchange_name:  # do not declare default exchange (#1295)
                try:
                    self.channel.exchange_declare(exchange=self.exchange_name,
                                                  exchange_type=self.exchange_type,
                                                  durable=self.exchange_durable)
                except pika.exceptions.ChannelClosed:
                    self.logger.error('Access to exchange refused.')
                    raise
            self.channel.confirm_delivery()

    def process(self):
        ''' Stop the Bot if cannot connect to AMQP Server after the defined connection attempts '''

        # self._connection and self.channel can be None
        if getattr(self._connection, 'is_closed', None) or getattr(self.channel, 'is_closed', None):
            self.connect_server()

        event = self.receive_message()
        body = self.export_event(event, return_type=str)

        # replace unicode characters when encoding (#1296)
        body = body.encode(errors='backslashreplace')
        if self.format_routing_key:
            routing_key = self.routing_key.format(ev=event)
        else:
            routing_key = self.routing_key

        try:
            if not self.channel.basic_publish(exchange=self.exchange_name,
                                              routing_key=routing_key,
                                              body=body,
                                              properties=self.properties,
                                              mandatory=True):
                if self.require_confirmation and not self.publish_raises_nack:
                    raise ValueError('Message sent but not confirmed.')
                elif not self.publish_raises_nack:
                    self.logger.info('Message sent but not confirmed.')
        except (pika.exceptions.ChannelError, pika.exceptions.AMQPChannelError,
                pika.exceptions.NackError):
            self.logger.exception('Error publishing the message.')
        except pika.exceptions.UnroutableError:
            self.logger.exception('The destination queue does not exist, declare it first. See also the README.')
            self.stop()
        else:
            self.acknowledge_message()

    def shutdown(self):
        if self._connection:
            self._connection.close()


BOT = AMQPTopicOutputBot
