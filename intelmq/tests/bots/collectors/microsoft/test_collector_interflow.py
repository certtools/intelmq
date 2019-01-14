"""
Test for the Microsoft Azure Collector Bot
"""

import datetime
import unittest

import intelmq.lib.test as test
from intelmq.bots.collectors.microsoft.collector_interflow import \
    MicrosoftInterflowCollectorBot

EXPECTED_MESSAGE = ("The cache's TTL must be higher than 'not_older_than', "
                    "otherwise the bot is processing the same data over and over again.")
class TestMicrosoftInterflowCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for MicrosoftInterflowCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MicrosoftInterflowCollectorBot
        cls.sysconfig = {'api_key': True,
                         'file_match': '',
                         'not_older_than': '1 day',
                         'redis_cache_ttl': 10,
                         }
        cls.use_cache = True

    def test_low_ttl_relative(self):
        with self.assertRaises(ValueError) as cm:
            self.prepare_bot()
        self.assertEqual(str(cm.exception), EXPECTED_MESSAGE)

    def test_high_ttl_relative(self):
        self.prepare_bot(parameters={'redis_cache_ttl': 600000})

    def test_low_ttl_absolute(self):
        with self.assertRaises(ValueError) as cm:
            self.prepare_bot(parameters={'not_older_than': '2019-01-01 00:00:00+00:00'})
        self.assertEqual(str(cm.exception), EXPECTED_MESSAGE)

    def test_high_ttl_absolute(self):
        self.prepare_bot(parameters={'not_older_than': datetime.datetime.now().isoformat()})
