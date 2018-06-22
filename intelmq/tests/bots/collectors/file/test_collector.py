# -*- coding: utf-8 -*-
"""
Testing File Collector
"""
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.file.collector_file import FileCollectorBot

PATH = os.path.join(os.path.dirname(__file__), 'testfile.txt')
with open(PATH) as handle:
    EXAMPLE_FILE = handle.read()

OUTPUT = {"__type": "Report",
          "feed.name": "Example feed",
          "feed.accuracy": 100.,
          "feed.url": "file://localhost" + PATH,
          "raw": utils.base64_encode(EXAMPLE_FILE),
          }


class TestFileCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FileCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FileCollectorBot
        file_path = os.path.dirname(__file__)
        cls.sysconfig = {'path': file_path,
                         'postfix': '.txt',
                         'delete_file': False,
                         'name': 'Example feed',
                         'chunk_size': None,
                         'chunk_replicate_header': True,
                         }

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.run_bot(iterations=1)

        self.assertMessageEqual(0, OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
