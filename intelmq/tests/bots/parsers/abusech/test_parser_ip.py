# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.abusech.parser_ip import AbusechIPParserBot

EXAMPLE_REPORT = {"feed.url": "https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist",
                  "feed.name": "AbuseCH Palevotracker",
                  "__type": "Report",
                  "source.ip": "103.232.215.133",
                  "raw": "MTAzLjIzMi4yMTUuMTMz",
                  "time.observation": "2015-11-02T13:11:44+00:00"
                  }

EXAMPLE_EVENT = { "feed.url": "https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist",
                  "feed.name": "AbuseCH Palevotracker",
                  "source.ip": "103.232.215.133",
                  "raw": "MTAzLjIzMi4yMTUuMTMz",
                  "time.observation": "2015-11-02T13:11:44+00:00",
                  "classification.type": "c&c",
                  "malware.name": "palevo",
                  "__type": "Event"
                  }


class TestAbusechIPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusechIPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechIPParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
