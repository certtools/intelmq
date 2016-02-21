# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.blueliv.parser_crimeserver import \
    BluelivCrimeserverParserBot


with open(os.path.join(os.path.dirname(__file__),
                       'test_parser_crimeserver.data')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Blueliv Crimeserver",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-09-02T14:17:58+00:00"
                  }
EXAMPLE_EVENT = {
    "__type": "Event",
    "feed.name": "Blueliv Crimeserver",
    "classification.type": "malware",
    "raw": "eyJjb3VudHJ5IjogIlVTIiwgImZpcnN0U2VlbkF0IjogIjIwMTUtMTAtMjBUMDY6MTQ6MDArMDAwMCIsICJpcCI6ICIxOTkuMzQuMjI4LjU0IiwgImxhc3RTZWVuQXQiOiAiMjAxNS0xMi0wOVQwNDo0MzoyOSswMDAwIiwgImxhdGl0dWRlIjogMzcuNzk4OSwgImxvbmdpdHVkZSI6IC0xMjIuMzk4NCwgInN0YXR1cyI6ICJPTkxJTkUiLCAidHlwZSI6ICJNQUxXQVJFIiwgInVwZGF0ZWRBdCI6ICIyMDE1LTEyLTA5VDA0OjQ1OjUzKzAwMDAiLCAidXJsIjogImh0dHA6Ly9hbWlyb3N0ZXJ3ZWlsLndlZWJseS5jb20vdXBsb2Fkcy8yLzMvMi81LzIzMjU4NTc2L2NvcnBvcmF0ZV9lbGVhcm5pbmcucGRmIn0=",  # nopep8
    "source.url": "http://amirosterweil.weebly.com/uploads/2/3/2/5/23258576/corporate_elearning.pdf",
    "time.source": "2015-10-20T06:14:00+00:00",
    "time.observation": "2015-09-02T14:17:58+00:00",
    "source.geolocation.cc": "US",
    "source.ip": "199.34.228.54"
}


class TestBluelivCrimeserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BluelivCrimeserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BluelivCrimeserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

if __name__ == '__main__':
    unittest.main()
