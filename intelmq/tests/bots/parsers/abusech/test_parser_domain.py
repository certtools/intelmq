# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.abusech.parser_domain import AbusechDomainParserBot

EXAMPLE_REPORT = {"feed.url": "https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist",
                  "feed.name": "AbuseCH Palevotracker",
                  "__type": "Report",
                  "source.fqdn": "arta.romail3arnest.info",
                  "raw": "YXJ0YS5yb21haWwzYXJuZXN0LmluZm8=",
                  "time.observation": "2015-11-02T13:11:43+00:00"
                  }

EXAMPLE_EVENT = {"feed.url": "https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist",
                 "feed.name": "AbuseCH Palevotracker",
                 "source.fqdn": "arta.romail3arnest.info",
                 "raw": "YXJ0YS5yb21haWwzYXJuZXN0LmluZm8=",
                 "time.observation": "2015-11-02T13:11:44+00:00",
                 "classification.type": "c&c",
                 "malware.name": "palevo",
                 "__type": "Event"
                 }


class TestAbusechDomainParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusechDomainParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechDomainParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
