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
from intelmq.bots.experts.http.expert_status import HttpStatusExpertBot

EXAMPLE_INPUT1 = {"__type": "Event",
                 "source.url": "http://localhost/foo",
                 "destination.url": "http://localhost/bar",
                 }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                 "source.url": "http://localhost/foo",
                 "destination.url": "http://localhost/bar",
                 "status": "online",
                 }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                 "source.url": "http://localhost/foo",
                 "destination.url": "http://localhost/bar",
                 "status": "offline",
                 }

def prepare_mocker(mocker):
    mocker.get('http://localhost/foo', status_code=200)
    mocker.get('http://localhost/bar', status_code=404)


@requests_mock.Mocker()
class TestHTTPStatusExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HTTPStatusExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HttpStatusExpertBot

    def test_status_200(self, mocker):
        """ Test with HTTP Status code 200. """
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_status_404(self, mocker):
        """ Test with HTTP Status code 404 and a custom field. """
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT1
        self.prepare_bot(parameters={'field': 'destination.url'})
        self.run_bot(prepare=False)
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
