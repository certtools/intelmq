# -*- coding: utf-8 -*-

import os
import os.path
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

REPORTS = {}
for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'testdata')):
    if not filename.endswith('.csv'):
        continue
    with open(os.path.join(os.path.dirname(__file__), 'testdata', filename)) as handle:
        EXAMPLE_FILE = handle.read()
    shortname = os.path.splitext(filename)[0]
    REPORTS[shortname] = {"raw": utils.base64_encode(EXAMPLE_FILE),
                          "__type": "Report",
                          "time.observation": "2015-01-01T00:00:00+00:00",
                          }


def generate_feed_function(feedname):
    def test_feed(self):
        """ Test if no errors happen for feed %s. """ % feedname
        self.sysconfig = {'feedname': feedname}
        self.input_message = REPORTS[feedname]
        self.run_bot()
    return test_feed


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.sysconfig = {'feedname': 'Accessible-CWMP'}


for key in REPORTS:
    setattr(TestShadowserverParserBot, 'test_feed_%s' % key, generate_feed_function(key))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
