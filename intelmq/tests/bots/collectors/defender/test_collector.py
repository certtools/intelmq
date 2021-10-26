# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import unittest
from unittest.mock import patch

import intelmq.lib.test as test
from intelmq.lib.utils import base64_encode
from intelmq.bots.collectors.defender.collector_defender import DefenderCollectorBot


class Mock_Response:
    """A mocked HTTP response, as from Requests.

    Returns the JSON dump of the Python structure given when creating
    the object.
    """
    text: str = ""
    status_code = 200

    def __init__(self, structure):
        self.text = json.dumps(structure)


class Mock_API_Endpoint:
    """A mocked REST API endpoint, suitable for calling using
    Requests.get().

    Returns Mock_Response objects containing static strings.
    """
    api_uri = ""
    responses = {}

    def __init__(self, api_uri="", responses={}):
        """Create a mocked API endpoint.

        Parameters:
        api_uri (str): Base URI of the API endpoint
        responses {str: str}: hash of {route1: response1, ...}

        A call to "api_uri/routeX" will receive a Mock_Response object
        containing "responseX".
        """
        self.api_uri = api_uri
        self.responses = responses

    def __call__(self, url, data=None):
        for prefix in self.responses.items():
            if url.startswith(self.api_uri + "/" + prefix[0]):
                return Mock_Response(prefix[1])

        return Mock_Response("Mock API called with unknown URL: " + url)


@test.skip_exotic()
class TestDefenderCollectorBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DefenderCollectorBot
        cls.sysconfig = {
            "tenant_id": "test_tenant_id",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "rate_limit": 2
        }

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_api_error(self, oauth2_get_mock, oauth2_fetch_token_mock):
        oauth2_get_mock.return_value = Mock_Response({"error": "Test error"})
        self.allowed_error_count = 1
        self.run_bot()
        self.assertRegexpMatchesLog(pattern="API error: Test error.")

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_empty_api_response(self, oauth2_get_mock, oauth2_fetch_token_mock):
        oauth2_get_mock.return_value = Mock_Response({"value": []})
        self.run_bot()
        self.assertOutputQueueLen(0)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_empty_alert(self, oauth2_get_mock, oauth2_fetch_token_mock):
        empty_alert = {}
        oauth2_get_mock.side_effect = Mock_API_Endpoint("https://api.securitycenter.windows.com/api",
                                                        {"alerts": {"value": [empty_alert]}})
        self.run_bot()
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0,
                                {
                                    "__type": "Report",
                                    "feed.accuracy": 100.0,
                                    "feed.name": "Test Bot",
                                    "feed.url": "https://api.securitycenter.windows.com/api",
                                    "raw": base64_encode(json.dumps(empty_alert))
                                })

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_multiple_alerts(self, oauth2_get_mock, oauth2_fetch_token_mock):
        alerts = [
            {
                "id": "abc123",
                "category": "Test",
                "evidence": [{
                    "entityType": "User",
                    "accountName": "test"
                }]
            },
            {
                "id": "def456",
                "category": "Test",
                "evidence": [{
                    "entityType": "User",
                    "accountName": "test2"
                }]
            }
        ]
        oauth2_get_mock.side_effect = Mock_API_Endpoint("https://api.securitycenter.windows.com/api",
                                                        {"alerts": {"value": alerts}})
        self.run_bot()
        self.assertOutputQueueLen(2)
        self.assertMessageEqual(0,
                                {
                                    "__type": "Report",
                                    "feed.accuracy": 100.0,
                                    "feed.name": "Test Bot",
                                    "feed.url": "https://api.securitycenter.windows.com/api",
                                    "raw": base64_encode(json.dumps(alerts[0]))
                                })
        self.assertMessageEqual(1,
                                {
                                    "__type": "Report",
                                    "feed.accuracy": 100.0,
                                    "feed.name": "Test Bot",
                                    "feed.url": "https://api.securitycenter.windows.com/api",
                                    "raw": base64_encode(json.dumps(alerts[1]))
                                })


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
