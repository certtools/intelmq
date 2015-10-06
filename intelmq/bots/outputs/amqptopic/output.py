# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pika
import sys
import time

from intelmq.lib.bot import Bot


class AMQPTopicBot(Bot):

    CONTENT_TYPE = 'application/json'
    DELIVERY_MODE = 1

    def init(self):
        self._connection = None
        self._channel = None
        self._url = self.parameters.url
        self._retries = self.parameters.retries
        self._maxerrors = self.parameters.maxerrors
        self._delay = self.parameters.delay
        self._exchange = self.parameters.exchange
        self._routing_key = self.parameters.routingkey
        self.connect_server()

    def connect_server(self):
        self.logger.info("Connecting to %s", self._url)
        for i in range(0, self._retries):
            try:
                self._connection = pika.BlockingConnection(
                    pika.URLParameters(self._url))
                break
            except pika.exceptions.AMQPConnectionError:
                self.logger.info(
                    'Could not connect to server. Retrying... (%d/%d)' % (i + 1, self._retries + 1))
                time.sleep(self._delay)
            except Exception, e:
                self.logger.exception('Unknown exception: %s', e)

        # connection error
        if self._connection is None:
            self.logger.error('Connection retries exceeded: %d', self._retries)
            # stop the bot
            self.stop()

        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self._exchange, type='topic')
        self._channel.confirm_delivery()

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        # verify | set connection
        if None in (self._connection, self._channel):
            self.connect_server()

        properties = pika.BasicProperties(
            content_type=self.CONTENT_TYPE, delivery_mode=self.DELIVERY_MODE)

        try:
            if not self._channel.basic_publish(exchange=self._exchange, routing_key=self._routing_key, body=event.to_json(), properties=properties, mandatory=True):
                self.logger.error("Message sent but not confirmed")
            self._errors = 0
        except Exception, e:
            self.logger.error("Error publishing the message: %s", e)
            if self._maxerrors > 0:
                self._errors += 1
                if self._errors == self._maxerrors:
                    self.logger.error('Max errors limit reached!')
                    self.acknowledge_message()
                    self.stop()

        self.acknowledge_message()


if __name__ == "__main__":
    bot = AMQPTopicBot(sys.argv[1])
    bot.start()
