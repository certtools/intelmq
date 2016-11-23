# -*- coding utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.nothink.parser import NothinkParserBot

with open(os.path.join(os.path.dirname(__file__), 'blacklist_snmp_day.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {'feed.url': 'http://www.nothink.org/blacklist/blacklist_snmp_day.txt',
                  'feed.name': 'Nothink SNMP',
                  '__type': 'Report',
                  'raw': utils.base64_encode(EXAMPLE_FILE),
                  'time.observation': '2016-11-15T10:00:15+00:00'
                  }

EXAMPLE_EVENT = {'feed.url': 'http://www.nothink.org/blacklist/blacklist_snmp_day.txt',
                 'feed.name': 'Nothink SNMP',
                 'source.ip': '185.128.40.162',
                 'raw': 'MTg1LjEyOC40MC4xNjI=',
                 'time.source': '2016-11-14T23:02:04+00:00',
                 'classification.type': 'scanner',
                 'protocol.application': 'snmp',
                 '__type': 'Event'
                 }


class TestNothinkParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase of NothinkParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = NothinkParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
