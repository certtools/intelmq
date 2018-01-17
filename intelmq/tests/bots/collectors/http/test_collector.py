# -*- coding: utf-8 -*-
"""
Testing HTTP collector
"""

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.collectors.http.collector_http import HTTPCollectorBot


OUTPUT = [{"__type": "Report",
           "feed.name": "Example feed",
           "feed.accuracy": 100.,
           "feed.url": "http://localhost/two_files.tar.gz",
           "raw": utils.base64_encode('bar text\n'),
           },
          {"__type": "Report",
           "feed.name": "Example feed",
           "feed.accuracy": 100.,
           "feed.url": "http://localhost/two_files.tar.gz",
           "raw": utils.base64_encode('foo text\n'),
           },
          ]


@test.skip_local_web()
class TestHTTPCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HTTPCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTTPCollectorBot
        cls.sysconfig = {'http_url': 'http://localhost/two_files.tar.gz',
                         'extract_files': True,
                         'feed': 'Example feed',
                         }

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = None
        self.run_bot(iterations=1)

        self.assertMessageEqual(0, OUTPUT[0])
        self.assertMessageEqual(1, OUTPUT[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
