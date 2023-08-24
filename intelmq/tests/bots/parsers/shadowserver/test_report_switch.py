# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/test_smb.csv')) as handle:
    EXAMPLE_LINES = handle.read().splitlines()[:2]

FIRST_REPORT = {'feed.name': 'Test-Accessible-SMB',
                "raw": utils.base64_encode('\n'.join(EXAMPLE_LINES)),
                "__type": "Report",
                "time.observation": "2019-03-25T00:00:00+00:00",
                "extra.file_name": "2019-03-25-test_smb-test-test.csv",
                }
with open(os.path.join(os.path.dirname(__file__), 'testdata/test_telnet.csv')) as handle:
    EXAMPLE_LINES = handle.read().splitlines()[:2]

SECOND_REPORT = {
    'feed.name': 'Test-Accessible-Telnet',
    "raw": utils.base64_encode('\n'.join(EXAMPLE_LINES)),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.file_name": "2019-01-01-test_telnet-test-geo.csv",
}


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = SECOND_REPORT
        cls.sysconfig = {'logging_level': 'DEBUG'}

    def test_event(self):
        """ Test if the parser correctly detects and handles different report types. """
        self.prepare_bot(parameters={'test_mode': True})
        self.input_message = [FIRST_REPORT, SECOND_REPORT]
        self.run_bot(iterations=2)
        self.assertLogMatches("Detected report's file name: 'test_smb'",
                              levelname='DEBUG')
        self.assertLogMatches("Detected report's file name: 'test_telnet'",
                              levelname='DEBUG')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
