# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.bambenek.parser_dgafeed import BambenekDGAfeedParserBot

with open(os.path.join(os.path.dirname(__file__), 'dga-feed.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Bambenek DGA Domain Feed",
                  "feed.url": "http://osint.bambenekconsulting.com/feeds/dga-feed.txt",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2016-01-01T00:00:00+00:00",
                 }
EVENTS = [{"feed.name": "Bambenek DGA Domain Feed",
           "feed.url": "http://osint.bambenekconsulting.com/feeds/dga-feed.txt",
           "__type": "Event",
           "time.source": "2016-11-10T00:00:00+00:00",
           "destination.fqdn": "xqmclnusaswvof.com",
           "classification.type": "ransomware",
           "time.observation": "2016-01-01T00:00:00+00:00",
           "event_description.text": "Domain used by Cryptolocker - Flashback DGA for 10 Nov 2016",
           "event_description.url": "http://osint.bambenekconsulting.com/manual/cl.txt",
           "raw": "eHFtY2xudXNhc3d2b2YuY29tLERvbWFpbiB1c2VkIGJ5IENyeXB0b2xvY2tlciAtIEZsYXNoYmFjayBER0EgZm9yIDEwIE5vdiAyMDE2LDIwMTYtMTEtMTAsaHR0cDovL29zaW50LmJhbWJlbmVrY29uc3VsdGluZy5jb20vbWFudWFsL2NsLnR4dA==",
          }]

class TestBambenekDGAfeedParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BambenekDGAfeedParserBot
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BambenekDGAfeedParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])

if __name__ == '__main__':
    unittest.main()
