# SPDX-FileCopyrightText: 2024 Manuel Subredu
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.extra_tags.expert import ExtraTagsExpertBot

MOCK_01_INPUT = {
    "__type": "Event",
    "time.observation": "2015-01-01T00:00:00+00:00",
}
MOCK_01_OUTPUT = {
    "__type": "Event",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.tags": {
        'is_dev': True
    }
}

MOCK_02_INPUT = {
    "__type": "Event",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.tags": {
        'constituent': 'univ_01'
    }
}
MOCK_02_OUTPUT = {
    "__type": "Event",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.tags": {
        'is_dev': True,
        'constituent': 'univ_01'
    }
}

MOCK_03_INPUT = {
    "__type": "Event",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.tags": {
        'constituent': 'univ_01',
        'is_dev': False
    }
}
MOCK_03_OUTPUT = {
    "__type": "Event",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.tags": {
        'is_dev': False,
        'constituent': 'univ_01'
    }
}

#@test.skip_exotic()
class TestExtraTagsExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for GeohashExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ExtraTagsExpertBot
        cls.sysconfig = {'overwrite': True, 'tags': {'is_dev': True}}

    def test_no_existing_tag(self):
        self.input_message = MOCK_01_INPUT
        self.run_bot()
        self.assertMessageEqual(0, MOCK_01_OUTPUT)

    def test_add_to_existing_tags(self):
        self.input_message = MOCK_02_INPUT
        self.run_bot()
        self.assertMessageEqual(0, MOCK_02_OUTPUT)

    def test_skip_existing_tag(self):
        self.sysconfig['overwrite'] = False

        self.input_message = MOCK_03_INPUT
        self.run_bot()
        self.assertMessageEqual(0, MOCK_03_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
