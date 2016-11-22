# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malc0de.parser_domain_blacklist import \
    Malc0deDomainBlacklistParserBot

with open(os.path.join(os.path.dirname(__file__), 'BOOT'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'malware',
           'raw': 'UFJJTUFSWSBleGFtcGxlLmNvbSBibG9ja2VkZG9tYWluLmhvc3Rz',
           'source.fqdn': 'example.com'}
OUTPUT2 = {'__type': 'Event',
           'classification.type': 'malware',
           'raw': 'UFJJTUFSWSBleGFtcGxlLm9yZyBibG9ja2VkZG9tYWluLmhvc3Rz',
           'source.fqdn': 'example.org'}


class TestMalc0deDomainBlacklistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Malc0deDomainBlacklistParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Malc0deDomainBlacklistParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
