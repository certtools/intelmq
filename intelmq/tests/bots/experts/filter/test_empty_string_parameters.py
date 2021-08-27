# SPDX-FileCopyrightText: 2021 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot
from .test_extra import EXAMPLE_INPUT


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilterExpertBot
        cls.input_message = EXAMPLE_INPUT
        cls.sysconfig = {'filter_key': 'source.asn',
                         'filter_value': '',
                         'filter_action': 'drop',
                         'not_before': '',
                         'not_after': ''}

    def test_empty_string_parameters(self):
        self.run_bot()
        # we actually only need to check if the bot does not fail
        self.assertMessageEqual(0, EXAMPLE_INPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
