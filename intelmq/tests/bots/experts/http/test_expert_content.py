# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing HTTP Status expert
"""
import unittest
import requests_mock

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.experts.http.expert_content import HttpContentExpertBot

EXAMPLE_INPUT1 = {"__type": "Event",
                 "source.url": "http://localhost/foo",
                 }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                 "source.url": "http://localhost/foo",
                 "status": "online",
                 }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                 "extra.reason": "Text Nonexistent response not found in response from http://localhost/foo",
                 "source.url": "http://localhost/foo",
                 "status": "offline",
                 }

def prepare_mocker(mocker):
    mocker.get('http://localhost/foo', text='Some response')


@requests_mock.Mocker()
class TestHTTPContentExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HTTPStatusExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HttpContentExpertBot

    def test_content_exists(self, mocker):
        """Test with existing content."""
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT1
        self.prepare_bot(parameters={'needle': 'Some response'})
        self.run_bot(prepare=False)
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_content_does_not_exist(self, mocker):
        """Test with content that does not exist."""
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT1
        self.prepare_bot(parameters={'needle': 'Nonexistent response'})
        self.run_bot(prepare=False)
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
