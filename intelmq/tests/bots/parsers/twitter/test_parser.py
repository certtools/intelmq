# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology, Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing the deprecation warning for Twitter Parser
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.twitter.parser import TwitterParserBot


@test.skip_exotic()
class TestTwitterParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(self):
        self.bot_reference = TwitterParserBot
        self.allowed_warning_count = 1
        self.skip_checks = True

    def test(self):
        self.run_bot()
        self.assertLogMatches(pattern=".*deprecated.*", levelname="WARNING")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
