# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.netlab_360.parser_dga import Netlab360DGAParserBot

with open(os.path.join(os.path.dirname(__file__), 'dga.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Netlab 360 DGA",
                  "feed.url": "http://data.netlab.360.com/feeds/dga/dga.txt",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2016-01-01T00:00:00+00:00",
                  }
EVENTS = [{"feed.name": "Netlab 360 DGA",
           "feed.url": "http://data.netlab.360.com/feeds/dga/dga.txt",
           "__type": "Event",
           "time.source": "2016-11-13T00:04:15+00:00",
           "source.fqdn": "difficultdress.net",
           "classification.type": "c&c",
           "time.observation": "2016-01-01T00:00:00+00:00",
           "classification.identifier": "suppobox",
           "event_description.url": "http://data.netlab.360.com/dga",
           "raw": "c3VwcG9ib3gJZGlmZmljdWx0ZHJlc3MubmV0CTIwMTYtMTEtMTIgMTE6NTg6NTYJMjAxNi0xMS0xMyAwMDowNDoxNQ==",
           }]


class TestNetlab360DGAParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Netlab360DGAParserBot
    """
    @classmethod
    def set_bot(cls):
        cls.bot_reference = Netlab360DGAParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
