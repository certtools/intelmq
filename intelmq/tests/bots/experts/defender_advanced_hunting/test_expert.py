# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import unittest
from copy import deepcopy
from unittest.mock import patch

import intelmq.lib.test as test
from intelmq.bots.experts.defender_advanced_hunting.expert import DefenderAdvancedHuntingExpertBot

EVENT_BASE = {
    "feed.url": "https://api.securitycenter.windows.com/api",
    "feed.name": "Defender advanced hunting test",
    "__type": "Event",
    "time.observation": "2021-05-25T06:06:06+00:00",
    "extra.deviceid": "abc123"
}


class Mock_Response:
    """A mocked HTTP response, as from Requests.

    Returns the JSON dump of the Python structure given when creating
    the object.
    """
    text: str = ""
    status_code = 200

    def __init__(self, structure):
        self.text = json.dumps(structure)


@test.skip_exotic()
class TestDefenderAdvancedHuntingExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DefenderAdvancedHuntingExpertBot
        cls.sysconfig = {
            "tenant_id": "test_tenant_id",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "query": 'DeviceEvents | where DeviceId == "{{ event["extra.deviceid"] }}"',
            "result_fields": {"username": "source.account"}
        }

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_jinja_substitution(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "test"}]})

        self.input_message = event
        self.run_bot()
        self.assertAnyLoglineEqual(
            levelname="DEBUG",
            message='Running advanced hunting query: "DeviceEvents | where DeviceId == \\"abc123\\"".'
        )

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_no_results(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        oauth2_post_mock.return_value = Mock_Response({"Results": []})

        self.input_message = event
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertAnyLoglineEqual(levelname="WARNING", message="No results returned.")
        self.assertMessageEqual(0, event)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_one_result(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        result = deepcopy(event)
        result["source.account"] = "test"

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "test"}]})

        self.input_message = event
        self.run_bot()
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_multiple_results_use_first(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        result = deepcopy(event)
        result["source.account"] = "test1"

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "test1"},
                                                                   {"username": "test2"}]})

        self.input_message = event
        self.prepare_bot(parameters={
            "multiple_result_handling": ["warn", "use_first", "send"]
        })
        self.allowed_warning_count = 1
        self.run_bot(prepare=False)
        self.assertLogMatches(levelname="WARNING", pattern="Multiple results returned: ")
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_multiple_results_ignore(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "test1"},
                                                                   {"username": "test2"}]})

        self.input_message = event
        self.prepare_bot(parameters={
            "multiple_result_handling": ["ignore", "send"]
        })
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, event)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_multiple_results_drop(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "test1"},
                                                                   {"username": "test2"}]})

        self.input_message = event
        self.prepare_bot(parameters={
            "multiple_result_handling": ["drop"]
        })
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_multiple_results_limit(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "test1"}]})

        self.input_message = event
        self.prepare_bot(parameters={
            "multiple_result_handling": ["limit"]
        })
        self.run_bot(prepare=False)
        self.assertAnyLoglineEqual(
            levelname="DEBUG",
            message='Running advanced hunting query: "DeviceEvents | where DeviceId == \\"abc123\\" | limit 1".'
        )

        result = deepcopy(event)
        result["source.account"] = "test1"

        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_overwrite(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["source.account"] = "old"

        result = deepcopy(event)
        result["source.account"] = "new"

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "new"}]})

        self.input_message = event
        self.prepare_bot(parameters={
            "overwrite": True
        })
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.post')
    def test_keep(self, oauth2_post_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["source.account"] = "old"

        oauth2_post_mock.return_value = Mock_Response({"Results": [{"username": "new"}]})

        self.input_message = event
        self.prepare_bot(parameters={
            "overwrite": False
        })
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, event)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
