# -*- coding: utf-8 -*-
import json
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.outputs.amqptopic.output import AMQPTopicOutputBot
from intelmq.tests.bots.outputs.redis.test_output import EXAMPLE_EVENT

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import pika


class TestAMQPTopicOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AMQPTopicOutputBot
        cls.default_input_message = EXAMPLE_EVENT
        cls.sysconfig = {"connection_attempts": 3,
                        "connection_heartbeat": 3600,
                        "connection_host": "127.0.0.1",
                        "connection_port": 5672,
                        "connection_vhost": "/",
                        "content_type": "application/json",
                        "delivery_mode": 2,
                        "exchange_durable": True,
                        "exchange_name": "",
                        "exchange_type": "topic",
                        "keep_raw_field": True,
                        "message_hierarchical_output": False,
                        "message_with_type": True,
                        "message_jsondict_as_string": False,
                        "password": None,
                        "require_confirmation": True,
                        "routing_key": "test",
                        "username": None,
                        }

    def setup_channel(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost',
                port=5672,
                socket_timeout=10,
                virtual_host='/',
                ))
        channel = connection.channel()
        channel.confirm_delivery()
        channel.queue_declare(queue='test', durable=True,
                              arguments={'x-queue-mode': 'lazy'})
        channel.queue_delete(queue='test')  # "purge" it
        channel.queue_declare(queue='test', durable=True,
                              arguments={'x-queue-mode': 'lazy'})
        return channel

    @test.skip_exotic()
    def test_event(self):
        """ Test AMQP Topic output. """
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost',
                port=5672,
                socket_timeout=10,
                virtual_host='/',
                ))
        channel = connection.channel()
        channel.confirm_delivery()
        channel.queue_declare(queue='test', durable=True,
                              arguments={'x-queue-mode': 'lazy'})

        self.run_bot()

        # Get the message from AMQP
        method, header, body = next(channel.consume('test'))
        event = utils.decode(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

        self.assertIsInstance(event, str)
        event_dict = json.loads(event)
        self.assertDictEqual(EXAMPLE_EVENT, event_dict)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
