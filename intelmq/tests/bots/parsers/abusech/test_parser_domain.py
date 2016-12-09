# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_domain import AbusechDomainParserBot

with open(os.path.join(os.path.dirname(__file__), 'feododomains.txt')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {"feed.url": "https://feodotracker.abuse.ch/blocklist/?download=domainblocklist",
                  "feed.name": "AbuseCH Palevotracker",
                  "__type": "Report",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "time.observation": "2015-11-02T13:11:43+00:00"
                  }

EXAMPLE_EVENT = {"feed.url": "https://feodotracker.abuse.ch/blocklist/?download=domainblocklist",
                 "feed.name": "AbuseCH Palevotracker",
                 "source.fqdn": "arta.romail3arnest.info",
                 "raw": "YXJ0YS5yb21haWwzYXJuZXN0LmluZm8=",
                 "time.observation": "2015-11-02T13:11:44+00:00",
                 "time.source": "2016-02-23T14:55:49+00:00",
                 "classification.type": "c&c",
                 "malware.name": "cridex",
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


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
