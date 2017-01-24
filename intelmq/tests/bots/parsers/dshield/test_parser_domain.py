# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.dshield.parser_domain import DshieldDomainParserBot

with open(os.path.join(os.path.dirname(__file__), 'suspiciousdomains_High.txt')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {"feed.name": "DShield Suspicious Domains",
                  "feed.url": "https://www.dshield.org/feeds/suspiciousdomains_High.txt",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{"feed.name": "DShield Suspicious Domains",
           "feed.url": "https://www.dshield.org/feeds/suspiciousdomains_High.txt",
           "__type": "Event",
           "time.source": "2015-12-22T04:10:10+00:00",
           "source.fqdn": "example.com",
           "classification.type": "malware",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "raw": "ZXhhbXBsZS5jb20J",
           },
          {"feed.name": "DShield Suspicious Domains",
           "feed.url": "https://www.dshield.org/feeds/suspiciousdomains_High.txt",
           "__type": "Event",
           "time.source": "2015-12-22T04:10:10+00:00",
           "source.fqdn": "example.org",
           "classification.type": "malware",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "raw": "ZXhhbXBsZS5vcmcJ",
           }]


class TestDshieldDomainParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DshieldDomainParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DshieldDomainParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])
        self.assertMessageEqual(1, EVENTS[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
