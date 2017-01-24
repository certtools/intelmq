# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.alienvault.parser import AlienVaultParserBot

RAW = "MTkyLjAuMC4xIzQjMiNNYWxpY2lvdXMgSG9zdCNERSMjMCwxIzMKMTAuMC4wLjQjMyMyI1NjYW5uaW5nIEhvc3QjR0IjTG9uZG9uIzIsMyMxMQ=="
OUTPUT1 = {'__type': 'Event',
           'classification.type': 'malware',
           'raw': 'MTkyLjAuMC4xIzQjMiNNYWxpY2lvdXMgSG9zdCNERSMjMCwxIzM=',
           'source.geolocation.cc': 'DE',
           'source.geolocation.latitude': 0.,
           'source.geolocation.longitude': 1.,
           'source.ip': '192.0.0.1'}

OUTPUT2 = {'__type': 'Event',
           'classification.type': 'scanner',
           'raw': 'MTAuMC4wLjQjMyMyI1NjYW5uaW5nIEhvc3QjR0IjTG9uZG9uIzIsMyMxMQ==',
           'source.geolocation.cc': 'GB',
           'source.geolocation.city': 'London',
           'source.geolocation.latitude': 2.,
           'source.geolocation.longitude': 3.,
           'source.ip': '10.0.0.4'}


class TestAlienVaultParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AlienVaultParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AlienVaultParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
