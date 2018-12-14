# -*- coding: utf-8 -*-
"""
Testing Anyrun collector
"""

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.anyrun.collector_anyrun import AnyrunCollectorBot


OUTPUT = {"__type": "Report",
          "feed.name": "Anyrun",
          "feed.accuracy": 100,
          "feed.url": "http://localhost/anyrun_testing_feed.txt",
          "raw": utils.base64_encode('foo text\n'),
          }


@test.skip_local_web()
class TestAnyrunCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AnyrunCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AnyrunCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/anyrun_testing.txt',
                         'name': 'Anyrun'
                         }

    def test_events(self):
        self.run_bot(iterations=1)
        self.assertMessageEqual(0, OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
