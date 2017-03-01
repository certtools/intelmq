# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.dshield.parser_asn import DShieldASNParserBot

with open(os.path.join(os.path.dirname(__file__), 'asdetailsascii.html')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {"feed.name": "DShield AS",
                  "feed.url": "https://dshield.org/asdetailsascii.html?as=1",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{"feed.name": "DShield AS",
           "feed.url": "https://dshield.org/asdetailsascii.html?as=1",
           "__type": "Event",
           "time.source": "2015-12-22T11:09:07+00:00",
           "source.asn": 1,
           "source.ip": "109.230.148.140",
           "classification.type": "brute-force",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra": '{"last_seen": "2015-12-22", "reports": 85, "targets": 56}',
           "raw": "MTA5LjIzMC4xNDguMTQwCTg1CTU2CQkyMDE1LTEyLTIyCTIwMTUtMTItMjIgMTE6MDk6MDc=",
           },
          {"feed.name": "DShield AS",
           "feed.url": "https://dshield.org/asdetailsascii.html?as=1",
           "__type": "Event",
           "time.source": "2015-12-14T12:40:59+00:00",
           "source.asn": 1,
           "source.ip": "109.230.155.61",
           "classification.type": "brute-force",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra": '{"last_seen": "2015-12-10", "reports": 1, "targets": 1}',
           "raw": "MTA5LjIzMC4xNTUuMDYxCTEJMQkJMjAxNS0xMi0xMAkyMDE1LTEyLTE0IDEyOjQwOjU5",
           }]


class TestDShieldASNParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DShieldASNParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DShieldASNParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])
        self.assertMessageEqual(1, EVENTS[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
