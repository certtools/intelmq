# SPDX-FileCopyrightText: 2016 Dustin Demuth
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.filter.expert import FilterExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "unauthorised-information-modification",
                 "time.source": "2005-01-01T00:00:00+00:00",
                 "time.observation": "2015-09-12T00:00:00+00:00",
                 "feed.name": "test-feed",
                 "raw": "Cg=="
                 }


class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FilterExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilterExpertBot
        cls.default_input_message = EXAMPLE_INPUT
        cls.sysconfig = {'filter_action': 'keep',
                         'filter_regex': 'search',
                         'filter_key': 'feed.name',
                         'filter_value': 'feed'}

    def test_searchRegex(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
