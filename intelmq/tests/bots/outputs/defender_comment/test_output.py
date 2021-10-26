# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import unittest
from unittest.mock import patch

import intelmq.lib.test as test
from intelmq.bots.outputs.defender_comment.output import DefenderCommentOutputBot

ID = "abcde123456_-987654"
COMMENT = "Alert handled by IntelMQ."

EVENT_VALID = {
    "__type": "Event",
    "extra.defender_id": ID,
    "extra.defender_comment": COMMENT
}

EVENT_NO_ID = {
    "__type": "Event",
    "extra.defender_comment": COMMENT
}

EVENT_NO_COMMENT = {
    "__type": "Event",
    "extra.defender_id": ID
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
class TestDefenderCommentOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DefenderCommentOutputBot
        cls.sysconfig = {
            "tenant_id": "test_tenant_id",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "comment_field": "extra.defender_comment"
        }

    @patch("requests_oauthlib.OAuth2Session.fetch_token")
    @patch("requests_oauthlib.OAuth2Session.patch")
    def test_valid(self, oauth2_patch_mock, oauth2_fetch_token_mock):
        oauth2_patch_mock.return_value = Mock_Response({
            "id": ID,
            "comments": [{
                "comment": COMMENT,
                "createdBy": "Automation"
            }]})

        self.input_message = EVENT_VALID
        self.run_bot()
        self.assertOutputQueueLen(0)

    @patch("requests_oauthlib.OAuth2Session.fetch_token")
    @patch("requests_oauthlib.OAuth2Session.patch")
    def test_no_id(self, oauth2_patch_mock, oauth2_fetch_token_mock):
        oauth2_patch_mock.return_value = Mock_Response({
            "id": ID,
            "comments": [{
                "comment": COMMENT,
                "createdBy": "Automation"
            }]})

        self.allowed_error_count = 1
        self.input_message = EVENT_NO_ID
        self.run_bot()
        self.assertRegexpMatchesLog(pattern="Event did not contain a Defender ID:")
        self.assertOutputQueueLen(0)

    @patch("requests_oauthlib.OAuth2Session.fetch_token")
    @patch("requests_oauthlib.OAuth2Session.patch")
    def test_no_comment(self, oauth2_patch_mock, oauth2_fetch_token_mock):
        oauth2_patch_mock.return_value = Mock_Response({
            "id": ID,
            "comments": [{
                "comment": COMMENT,
                "createdBy": "Automation"
            }]})

        self.allowed_error_count = 1
        self.input_message = EVENT_NO_COMMENT
        self.run_bot()
        self.assertRegexpMatchesLog(pattern="Event did not contain a comment:")
        self.assertOutputQueueLen(0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
