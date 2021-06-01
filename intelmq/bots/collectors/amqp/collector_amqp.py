# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Collecting from a (remote) AMQP Server and fetching either intelmq or any other messages.
"""
import ssl

from intelmq.bots.outputs.amqptopic.output import AMQPTopicOutputBot
from intelmq.lib.bot import CollectorBot
from intelmq.lib.message import MessageFactory
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pika
except ImportError:
    pika = None


class AMQPCollectorBot(AMQPTopicOutputBot, CollectorBot):
    """
    Collect data from an AMQP Server and fetch either intelmq or any other messages. Requires the pika python library.
    Inheriting from AMQPTopicOutputBot for connect_server method
    """
    connection_attempts: int = 3
    connection_heartbeat: int = 3600
    connection_host: str = "127.0.0.1"  # TODO should be ipaddress
    connection_port: int = 5672
    connection_vhost: str = None
    expect_intelmq_message: bool = False
    password: str = None
    queue_name: str = None
    use_ssl: bool = False
    username: str = None

    def init(self):
        if pika is None:
            raise MissingDependencyError("pika", version=">=1.0")

        self.connection = None
        self.channel = None

        pika_version = tuple(int(x) for x in pika.__version__.split('.'))
        if pika_version < (1, ):
            raise MissingDependencyError("pika", version=">=1.0",
                                         installed=pika.__version__)

        self.kwargs = {}
        self.kwargs['heartbeat'] = self.connection_heartbeat

        if self.username and self.password:
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

        self.connect_server()

    def process(self):
        ''' Stop the Bot if cannot connect to AMQP Server after the defined connection attempts '''

        # self.connection and self.channel can be None
        if getattr(self.connection, 'is_closed', None) or getattr(self.channel, 'is_closed', None):
            self.connect_server()

        try:
            method, header, body = next(self.channel.consume(self.queue_name))
        except (pika.exceptions.ChannelError, pika.exceptions.AMQPChannelError):
            self.logger.exception('Error receiving messages.')
        else:
            if self.expect_intelmq_message:
                message = MessageFactory.unserialize(body.decode())
                self.send_message(message, auto_add=False)
            else:
                report = self.new_report()
                report['raw'] = body
                self.send_message(report)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)


BOT = AMQPCollectorBot
