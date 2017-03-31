# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.dshield.parser_block import DshieldBlockParserBot

with open(os.path.join(os.path.dirname(__file__), 'block.txt')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {"feed.name": "DShield Block",
                  "feed.url": "https://www.dshield.org/block.txt",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{"feed.name": "DShield Block",
           "feed.url": "https://www.dshield.org/block.txt",
           "__type": "Event",
           "time.source": "2015-12-15T15:33:38+00:00",
           "source.network": "43.229.53.0/24",
           "classification.type": "blacklist",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "source.geolocation.cc": "JP",
           "source.abuse_contact": "admin@v6nic.net",
           "extra": '{"attacks": 788, "network_name": "Japan Inet"}',
           "raw": "NDMuMjI5LjUzLjAJNDMuMjI5LjUzLjI1NQkyNAk3ODgJSmFwYW4gSW5ldAlKUAlhZG1pbkB2Nm5pYy5uZXQ=",
           },
          {"feed.name": "DShield Block",
           "feed.url": "https://www.dshield.org/block.txt",
           "__type": "Event",
           "time.source": "2015-12-15T15:33:38+00:00",
           "source.network": "194.63.140.0/24",
           "classification.type": "blacklist",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra": '{"attacks": 585}',
           "raw": "MTk0LjYzLjE0MC4wCTE5NC42My4xNDAuMjU1CTI0CTU4NQ==",
           }]


class TestDshieldBlockParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DshieldBlockParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DshieldBlockParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])
        self.assertMessageEqual(1, EVENTS[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
