# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.rsync.collector_rsync import RsyncCollectorBot

PATH = os.path.join(os.path.dirname(__file__), 'testfile.txt')
with open(PATH) as handle:
    EXAMPLE_FILE = handle.read()

OUTPUT = {"__type": "Report",
          "feed.name": "RsyncCollector",
          "feed.accuracy": 100.,
          "raw": utils.base64_encode(EXAMPLE_FILE),
          }


class TestRsyncCollectorBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = RsyncCollectorBot
        file_path = os.path.dirname(__file__)
        cls.sysconfig = {'rsync_path': file_path,
                         'file': "testfile.txt",
                         "name": "RsyncCollector"}

    def test_events(self):
        self.run_bot(iterations=1)
        self.assertMessageEqual(0, OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
