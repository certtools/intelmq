# SPDX-FileCopyrightText: 2022 gutsohnCERT
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing uri.
"""

import unittest
from rfc3986 import exceptions
import intelmq.lib.test as test
from intelmq.bots.experts.uri.expert import URIExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://example.com/something/index.php",
                 "destination.url": "http://example.org/download?file.exe",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.url": "http://example.com/something/index.php",
                  "destination.url": "http://example.org/download?file.exe",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "source.fqdn": "example.com",
                  "source.scheme": "http",
                  "source.path": "/something/index.php",
                  "destination.fqdn": "example.org",
                  "destination.scheme": "http",
                  "destination.path": "/download",
                  "destination.query": "file.exe",
                  }
IP_INPUT = {"__type": "Event",
            "source.url": "http://127.0.0.1/something/index.php",
            "destination.url": "http://[2001:db8::123]/download?file.exe",
            "time.observation": "2015-01-01T00:00:00+00:00"
            }
IP_OUTPUT = {"__type": "Event",
             "source.url": "http://127.0.0.1/something/index.php",
             "source.ip": "127.0.0.1",
             "destination.url": "http://[2001:db8::123]/download?file.exe",
             "time.observation": "2015-01-01T00:00:00+00:00",
             "source.scheme": "http",
             "source.path": "/something/index.php",
             "destination.scheme": "http",
             "destination.path": "/download",
             "destination.query": "file.exe",
             }


class TestURIExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for URIExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URIExpertBot

    def test_uri_correct_output(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_uri_overwrite(self):
        self.input_message = EXAMPLE_INPUT.copy()
        self.input_message['source.fqdn'] = 'example.net'
        self.sysconfig = {'overwrite': True}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_uri_ip(self):
        self.input_message = IP_INPUT.copy()
        self.run_bot()
        self.assertMessageEqual(0, IP_OUTPUT)

    # def test_invalid_uri(self):
    #
    #     with self.assertRaises(exceptions.MissingComponentError):
    #         self.input_message = EXAMPLE_INPUT.copy()
    #         self.input_message['source.url'] = '//example.net'
    #         self.run_bot()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
