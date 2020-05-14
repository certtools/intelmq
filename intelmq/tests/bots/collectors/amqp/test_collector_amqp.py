# -*- coding: utf-8 -*-
import json
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.amqp.collector_amqp import AMQPCollectorBot
from intelmq.tests.bots.outputs.redis.test_output import EXAMPLE_EVENT
from intelmq.tests.bots.outputs.amqptopic.test_output import TestAMQPTopicOutputBot


BODY_PLAIN = b'foobar This is a test'
REPORT_PLAIN = {'__type': 'Report',
                'raw': utils.base64_encode(BODY_PLAIN),
                "feed.name": "AMQP Feed",
                "feed.accuracy": 100.0,
                }


class TestAMQPCollectorBot(test.BotTestCase, unittest.TestCase):
    setup_channel = TestAMQPTopicOutputBot.setup_channel

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AMQPCollectorBot
        cls.sysconfig = {"connection_attempts": 3,
                         "connection_heartbeat": 3600,
                         "connection_host": "127.0.0.1",
                         "connection_port": 5672,
                         "connection_vhost": "/",
                         "password": None,
                         "username": None,
                         "queue_name": "test",
                         "name": "AMQP Feed",
                         }

    @test.skip_exotic()
    def test_report_plain(self):
        """ Test AMQP collectory with any message. """
        self.bot_type = 'collector'

        channel = self.setup_channel()
        channel.basic_publish(exchange='',
                              routing_key='test',
                              body=BODY_PLAIN,
                              mandatory=True)

        self.run_bot()
        self.assertMessageEqual(0, REPORT_PLAIN)

    @test.skip_exotic()
    def test_report_intelmq(self):
        """ Test AMQP collectory with an IntelMQ event. """
        self.bot_type = 'parser'

        channel = self.setup_channel()
        channel.basic_publish(exchange='',
                              routing_key='test',
                              body=json.dumps(EXAMPLE_EVENT),
                              mandatory=True)

        self.prepare_bot(parameters={'expect_intelmq_message': True})
        self.run_bot(prepare=False)
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
