# -*- coding: utf-8 -*-

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
    'extra': '{"confidence": 4, "status": "ONLINE", "time_last_seen": '
               '"2015-12-09T04:43:29+0000", "time_updated": '
               '"2015-12-09T04:45:53+0000"}',
    "raw": "eyJjb25maWRlbmNlIjogNCwgImNvdW50cnkiOiAiVVMiLCAiZmlyc3RTZWVuQXQiOiAiMjAxNS0xMC0yMFQwNjoxNDowMCswMDAwIiwgImlwIjogIjE5OS4zNC4yMjguNTQiLCAibGFzdFNlZW5BdCI6ICIyMDE1LTEyLTA5VDA0OjQzOjI5KzAwMDAiLCAibGF0aXR1ZGUiOiAzNy43OTg5LCAibG9uZ2l0dWRlIjogLTEyMi4zOTg0LCAic3RhdHVzIjogIk9OTElORSIsICJ0eXBlIjogIk1BTFdBUkUiLCAidXBkYXRlZEF0IjogIjIwMTUtMTItMDlUMDQ6NDU6NTMrMDAwMCIsICJ1cmwiOiAiaHR0cDovL2FtaXJvc3RlcndlaWwud2VlYmx5LmNvbS91cGxvYWRzLzIvMy8yLzUvMjMyNTg1NzYvY29ycG9yYXRlX2VsZWFybmluZy5wZGYifQ==",  # nopep8
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

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
