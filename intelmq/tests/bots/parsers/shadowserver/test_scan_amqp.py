# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
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
   'classification.identifier' : 'scan-amqp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.capabilities' : 'publisher_confirms,exchange_exchange_bindings,basic.nack,consumer_cancel_notify,connection.blocked,consumer_priorities,authentication_failure_close,per_consumer_qos',
   'extra.class' : '10',
   'extra.cluster_name' : 'rabbit@iZuf63m0nnq9bwf7lhjxrkZ',
   'extra.locales' : 'en_US',
   'extra.mechanisms' : 'PLAIN AMQPLAIN',
   'extra.message_length' : '509',
   'extra.method' : '10',
   'extra.platform' : 'Erlang/OTP',
   'extra.product' : 'RabbitMQ',
   'extra.product_version' : '3.3.5',
   'extra.source.naics' : 518210,
   'extra.tag' : 'amqp',
   'extra.version_minor' : '9',
   'feed.name' : 'Accessible AMQP',
   'protocol.application' : 'amqp',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJjaGFubmVsIiwibWVzc2FnZV9sZW5ndGgiLCJjbGFzcyIsIm1ldGhvZCIsInZlcnNpb25fbWFqb3IiLCJ2ZXJzaW9uX21pbm9yIiwiY2FwYWJpbGl0aWVzIiwiY2x1c3Rlcl9uYW1lIiwicGxhdGZvcm0iLCJwcm9kdWN0IiwicHJvZHVjdF92ZXJzaW9uIiwibWVjaGFuaXNtcyIsImxvY2FsZXMiCiIyMDIyLTAxLTEwIDA0OjMyOjEzIiwiNDcuMTAzLjAuMCIsInRjcCIsNTY3MiwsImFtcXAiLDM3OTYzLCJDTiIsIlNIQU5HSEFJIFNISSIsIlNIQU5HSEFJIiw1MTgyMTAsLDAsNTA5LDEwLDEwLDAsOSwicHVibGlzaGVyX2NvbmZpcm1zLGV4Y2hhbmdlX2V4Y2hhbmdlX2JpbmRpbmdzLGJhc2ljLm5hY2ssY29uc3VtZXJfY2FuY2VsX25vdGlmeSxjb25uZWN0aW9uLmJsb2NrZWQsY29uc3VtZXJfcHJpb3JpdGllcyxhdXRoZW50aWNhdGlvbl9mYWlsdXJlX2Nsb3NlLHBlcl9jb25zdW1lcl9xb3MiLCJyYWJiaXRAaVp1ZjYzbTBubnE5YndmN2xoanhya1oiLCJFcmxhbmcvT1RQIiwiUmFiYml0TVEiLCIzLjMuNSIsIlBMQUlOIEFNUVBMQUlOIiwiZW5fVVMi',
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
   'classification.identifier' : 'scan-amqp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.capabilities' : 'publisher_confirms,exchange_exchange_bindings,basic.nack,consumer_cancel_notify,connection.blocked,consumer_priorities,authentication_failure_close,per_consumer_qos,direct_reply_to',
   'extra.class' : '10',
   'extra.cluster_name' : 'rabbit@mtk-breizh',
   'extra.locales' : 'en_US',
   'extra.mechanisms' : 'AMQPLAIN PLAIN',
   'extra.message_length' : '509',
   'extra.method' : '10',
   'extra.platform' : 'Erlang/OTP 24.0.3',
   'extra.product' : 'RabbitMQ',
   'extra.product_version' : '3.8.19',
   'extra.source.naics' : 518210,
   'extra.tag' : 'amqp',
   'extra.version_minor' : '9',
   'feed.name' : 'Accessible AMQP',
   'protocol.application' : 'amqp',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJjaGFubmVsIiwibWVzc2FnZV9sZW5ndGgiLCJjbGFzcyIsIm1ldGhvZCIsInZlcnNpb25fbWFqb3IiLCJ2ZXJzaW9uX21pbm9yIiwiY2FwYWJpbGl0aWVzIiwiY2x1c3Rlcl9uYW1lIiwicGxhdGZvcm0iLCJwcm9kdWN0IiwicHJvZHVjdF92ZXJzaW9uIiwibWVjaGFuaXNtcyIsImxvY2FsZXMiCiIyMDIyLTAxLTEwIDA0OjMyOjEzIiwiMTQxLjk1LjAuMCIsInRjcCIsNTY3MiwsImFtcXAiLDE2Mjc2LCJERSIsIlNBQVJMQU5EIiwiU0FBUkJSVUNLRU4iLDUxODIxMCwsMCw1MDksMTAsMTAsMCw5LCJwdWJsaXNoZXJfY29uZmlybXMsZXhjaGFuZ2VfZXhjaGFuZ2VfYmluZGluZ3MsYmFzaWMubmFjayxjb25zdW1lcl9jYW5jZWxfbm90aWZ5LGNvbm5lY3Rpb24uYmxvY2tlZCxjb25zdW1lcl9wcmlvcml0aWVzLGF1dGhlbnRpY2F0aW9uX2ZhaWx1cmVfY2xvc2UscGVyX2NvbnN1bWVyX3FvcyxkaXJlY3RfcmVwbHlfdG8iLCJyYWJiaXRAbXRrLWJyZWl6aCIsIkVybGFuZy9PVFAgMjQuMC4zIiwiUmFiYml0TVEiLCIzLjguMTkiLCJBTVFQTEFJTiBQTEFJTiIsImVuX1VTIg==',
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
   'classification.identifier' : 'scan-amqp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.capabilities' : 'publisher_confirms,exchange_exchange_bindings,basic.nack,consumer_cancel_notify,connection.blocked,consumer_priorities,authentication_failure_close,per_consumer_qos,direct_reply_to',
   'extra.class' : '10',
   'extra.cluster_name' : 'rabbit@1397a0e9629b',
   'extra.locales' : 'en_US',
   'extra.mechanisms' : 'PLAIN AMQPLAIN',
   'extra.message_length' : '509',
   'extra.method' : '10',
   'extra.platform' : 'Erlang/OTP 24.2',
   'extra.product' : 'RabbitMQ',
   'extra.product_version' : '3.9.11',
   'extra.source.naics' : 454110,
   'extra.tag' : 'amqp',
   'extra.version_minor' : '9',
   'feed.name' : 'Accessible AMQP',
   'protocol.application' : 'amqp',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJjaGFubmVsIiwibWVzc2FnZV9sZW5ndGgiLCJjbGFzcyIsIm1ldGhvZCIsInZlcnNpb25fbWFqb3IiLCJ2ZXJzaW9uX21pbm9yIiwiY2FwYWJpbGl0aWVzIiwiY2x1c3Rlcl9uYW1lIiwicGxhdGZvcm0iLCJwcm9kdWN0IiwicHJvZHVjdF92ZXJzaW9uIiwibWVjaGFuaXNtcyIsImxvY2FsZXMiCiIyMDIyLTAxLTEwIDA0OjMyOjEzIiwiNTQuMjM0LjAuMCIsInRjcCIsNTY3MiwiZWMyLTU0LjIzNC4wLjAuY29tcHV0ZS0xLmFtYXpvbmF3cy5jb20iLCJhbXFwIiwxNDYxOCwiVVMiLCJWSVJHSU5JQSIsIkFTSEJVUk4iLDQ1NDExMCwsMCw1MDksMTAsMTAsMCw5LCJwdWJsaXNoZXJfY29uZmlybXMsZXhjaGFuZ2VfZXhjaGFuZ2VfYmluZGluZ3MsYmFzaWMubmFjayxjb25zdW1lcl9jYW5jZWxfbm90aWZ5LGNvbm5lY3Rpb24uYmxvY2tlZCxjb25zdW1lcl9wcmlvcml0aWVzLGF1dGhlbnRpY2F0aW9uX2ZhaWx1cmVfY2xvc2UscGVyX2NvbnN1bWVyX3FvcyxkaXJlY3RfcmVwbHlfdG8iLCJyYWJiaXRAMTM5N2EwZTk2MjliIiwiRXJsYW5nL09UUCAyNC4yIiwiUmFiYml0TVEiLCIzLjkuMTEiLCJQTEFJTiBBTVFQTEFJTiIsImVuX1VTIg==',
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
