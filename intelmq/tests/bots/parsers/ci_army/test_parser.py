# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.ci_army.parser import CIArmyParserBot

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'blacklist',
           'raw': 'MTAuMC4wLjk=',
           'source.ip': '10.0.0.9'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'blacklist',
           'raw': 'MTkyLjE2OC4wLjg=',
           'source.ip': '192.168.0.8'}


class TestCIArmyParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CIArmyParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CIArmyParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'MTAuMC4wLjkKMTkyLjE2OC4wLjgK'}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
