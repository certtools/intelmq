# -*- coding: utf-8 -*-
import tempfile
import os
import unittest
import shutil

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

@unittest.skipIf(shutil.which("rsync") is None, "RSync is not installed")
class TestRsyncCollectorBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = RsyncCollectorBot
        cls.base_dir = tempfile.TemporaryDirectory()
        file_path = os.path.dirname(__file__)
        cls.sysconfig = {'rsync_path': file_path,
                         'file': "testfile.txt",
                         "name": "RsyncCollector",
                         "temp_directory": cls.base_dir.name}

    def test_events(self):
        self.run_bot(iterations=1)
        self.assertMessageEqual(0, OUTPUT)

    def test_fail(self):
        self.allowed_error_count = 1
        self.run_bot(iterations=1, parameters={"rsync_path": "/foobar"})
        self.assertLogMatches('.*failed with exitcode.*')

    @classmethod
    def tearDownClass(cls):
        cls.base_dir.cleanup()
        super().tearDownClass()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
