# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_amqp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible AMQP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_amqp-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'accessible-amqp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.capabilities' : 'publisher_confirms,exchange_exchange_bindings,basic.nack,consumer_cancel_notify,connection.blocked,consumer_priorities,authentication_failure_close,per_consumer_qos',
   'extra.class' : '10',
   'extra.cluster_name' : 'rabbit@iZuf63m0nnq9bwf7lhjxrkZ',
   'extra.locales' : 'en_US',
   'extra.mechanisms' : 'PLAIN AMQPLAIN',
   'extra.message_length' : 509,
   'extra.method' : '10',
   'extra.platform' : 'Erlang/OTP',
   'extra.product' : 'RabbitMQ',
   'extra.product_version' : '3.3.5',
   'extra.naics' : 518210,
   'extra.tag' : 'amqp',
   'extra.version_minor' : '9',
   'feed.name' : 'Accessible AMQP',
   'protocol.application' : 'amqp',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 37963,
   'source.geolocation.cc' : 'CN',
   'source.geolocation.city' : 'SHANGHAI',
   'source.geolocation.region' : 'SHANGHAI SHI',
   'source.ip' : '47.103.0.0',
   'source.port' : 5672,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T04:32:13+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'accessible-amqp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.capabilities' : 'publisher_confirms,exchange_exchange_bindings,basic.nack,consumer_cancel_notify,connection.blocked,consumer_priorities,authentication_failure_close,per_consumer_qos,direct_reply_to',
   'extra.class' : '10',
   'extra.cluster_name' : 'rabbit@mtk-breizh',
   'extra.locales' : 'en_US',
   'extra.mechanisms' : 'AMQPLAIN PLAIN',
   'extra.message_length' : 509,
   'extra.method' : '10',
   'extra.platform' : 'Erlang/OTP 24.0.3',
   'extra.product' : 'RabbitMQ',
   'extra.product_version' : '3.8.19',
   'extra.naics' : 518210,
   'extra.tag' : 'amqp',
   'extra.version_minor' : '9',
   'feed.name' : 'Accessible AMQP',
   'protocol.application' : 'amqp',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 16276,
   'source.geolocation.cc' : 'DE',
   'source.geolocation.city' : 'SAARBRUCKEN',
   'source.geolocation.region' : 'SAARLAND',
   'source.ip' : '141.95.0.0',
   'source.port' : 5672,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T04:32:13+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'accessible-amqp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.capabilities' : 'publisher_confirms,exchange_exchange_bindings,basic.nack,consumer_cancel_notify,connection.blocked,consumer_priorities,authentication_failure_close,per_consumer_qos,direct_reply_to',
   'extra.class' : '10',
   'extra.cluster_name' : 'rabbit@1397a0e9629b',
   'extra.locales' : 'en_US',
   'extra.mechanisms' : 'PLAIN AMQPLAIN',
   'extra.message_length' : 509,
   'extra.method' : '10',
   'extra.platform' : 'Erlang/OTP 24.2',
   'extra.product' : 'RabbitMQ',
   'extra.product_version' : '3.9.11',
   'extra.naics' : 454110,
   'extra.tag' : 'amqp',
   'extra.version_minor' : '9',
   'feed.name' : 'Accessible AMQP',
   'protocol.application' : 'amqp',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 14618,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'ASHBURN',
   'source.geolocation.region' : 'VIRGINIA',
   'source.ip' : '54.234.0.0',
   'source.port' : 5672,
   'source.reverse_dns' : 'ec2-54.234.0.0.compute-1.amazonaws.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T04:32:13+00:00'
}
]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
