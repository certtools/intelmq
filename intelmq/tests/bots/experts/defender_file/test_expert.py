# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import unittest
from copy import deepcopy
from unittest.mock import patch

import intelmq.lib.test as test
from intelmq.bots.experts.defender_file.expert import DefenderFileExpertBot


FILE_EVIDENCE_EMPTY = {
    "entityType": "File",
    "evidenceCreationTime": "2021-05-25T05:05:05.1234567Z",
    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",  # The empty string
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "fileName": "empty.txt",
    "filePath": "C:\\Temp",
    "processId": None,
    "processCommandLine": None,
    "processCreationTime": None,
    "parentProcessId": None,
    "parentProcessCreationTime": None,
    "parentProcessFileName": None,
    "parentProcessFilePath": None,
    "ipAddress": None,
    "url": None,
    "registryKey": None,
    "registryHive": None,
    "registryValueType": None,
    "registryValue": None,
    "accountName": None,
    "domainName": None,
    "userSid": None,
    "aadUserId": None,
    "userPrincipalName": None,
    "detectionStatus": "Prevented"
}

FILE_EVIDENCE_A = {
    "entityType": "File",
    "evidenceCreationTime": "2021-05-25T06:06:06.1234567Z",
    "sha1": "3f786850e387550fdab836ed7e6dc881de23001b",  # 'a'
    "sha256": "87428fc522803d31065e7bce3cf03fe475096631e5e07bbd7a0fde60c4cf25c7",
    "fileName": "a.txt",
    "filePath": "C:\\Temp",
    "processId": None,
    "processCommandLine": None,
    "processCreationTime": None,
    "parentProcessId": None,
    "parentProcessCreationTime": None,
    "parentProcessFileName": None,
    "parentProcessFilePath": None,
    "ipAddress": None,
    "url": None,
    "registryKey": None,
    "registryHive": None,
    "registryValueType": None,
    "registryValue": None,
    "accountName": None,
    "domainName": None,
    "userSid": None,
    "aadUserId": None,
    "userPrincipalName": None,
    "detectionStatus": "Prevented"
}

FILEINFO_EMPTY = {
    "@odata.context": "https://api-eu.securitycenter.windows.com/api/$metadata#Files/$entity",
    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "md5": "d41d8cd98f00b204e9800998ecf8427e",
    "globalPrevalence": 4711,
    "globalFirstObserved": "1970-01-01T00:00:00.0Z",
    "globalLastObserved": "2021-05-25T10:10:10.1234567Z",
    "size": 0,
    "fileType": None,
    "isPeFile": False,
    "filePublisher": "Example Ltd",
    "fileProductName": "Empty Test File",
    "signer": "Example Ltd",
    "issuer": "Example CA",
    "signerHash": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "isValidCertificate": False,
    "determinationType": "Unknown",
    "determinationValue": "PUA:Win32/Empty"
}

FILEINFO_A = {
    "@odata.context": "https://api-eu.securitycenter.windows.com/api/$metadata#Files/$entity",
    "sha1": "3f786850e387550fdab836ed7e6dc881de23001b",  # "a"
    "sha256": "87428fc522803d31065e7bce3cf03fe475096631e5e07bbd7a0fde60c4cf25c7",
    "md5": "60b725f10c9c85c70d97880dfe8191b3",
    "globalPrevalence": 4711,
    "globalFirstObserved": "1970-01-01T01:01:01.0Z",
    "globalLastObserved": "2021-05-25T11:11:11.1234567Z",
    "size": 0,
    "fileType": None,
    "isPeFile": False,
    "filePublisher": "Example Ltd",
    "fileProductName": "Empty Test File",
    "signer": "Example Ltd",
    "issuer": "Example CA",
    "signerHash": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "isValidCertificate": False,
    "determinationType": "Unknown",
    "determinationValue": "PUA:Win32/A"
}

EVENT_BASE = {
    "feed.url": "https://api.securitycenter.windows.com/api",
    "feed.name": "Defender parser test",
    "__type": "Event",
    "time.observation": "2021-05-25T06:06:06+00:00",
    "extra.evidence": []
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
class TestDefenderFileExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DefenderFileExpertBot
        cls.sysconfig = {
            "tenant_id": "test_tenant_id",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "retries": 2,
            "min_wait": 1,
            "max_wait": 2
        }

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_api_error(self, oauth2_get_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["extra.evidence"] = [FILE_EVIDENCE_EMPTY]

        oauth2_get_mock.return_value = Mock_Response({"error": "Test error"})

        result = deepcopy(event)
        result["extra.fileinfo"] = []

        self.input_message = event
        self.allowed_warning_count = 4
        self.allowed_error_count = 1
        self.run_bot()
        self.assertRegexpMatchesLog(pattern=f"Error fetching file information for hash {event['extra.evidence'][0]['sha1']}: Test error.")
        self.assertRegexpMatchesLog(pattern=f"Error fetching file information for hash {event['extra.evidence'][0]['sha256']}: Test error.")
        self.assertRegexpMatchesLog(pattern=f"Max retries reached while fetching file information for hashes \['{event['extra.evidence'][0]['sha1']}', '{event['extra.evidence'][0]['sha256']}'\]")
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_not_found(self, oauth2_get_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["extra.evidence"] = [FILE_EVIDENCE_EMPTY]

        oauth2_get_mock.return_value = Mock_Response({"error": {"code": "NotFound"}})

        result = deepcopy(event)
        result["extra.fileinfo"] = []

        self.input_message = event
        self.allowed_warning_count = 4
        self.allowed_error_count = 1
        self.run_bot()
        self.assertRegexpMatchesLog(pattern=f"Error fetching file information for hash {event['extra.evidence'][0]['sha1']}: {{'code': 'NotFound'}}")
        self.assertRegexpMatchesLog(pattern=f"Error fetching file information for hash {event['extra.evidence'][0]['sha256']}: {{'code': 'NotFound'}}")
        self.assertRegexpMatchesLog(pattern=f"Max retries reached while fetching file information for hashes \['{event['extra.evidence'][0]['sha1']}', '{event['extra.evidence'][0]['sha256']}'\]")
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_single_file(self, oauth2_get_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["extra.evidence"] = [FILE_EVIDENCE_EMPTY]

        result = deepcopy(event)
        result["extra.fileinfo"] = [FILEINFO_EMPTY]

        oauth2_get_mock.return_value = Mock_Response(FILEINFO_EMPTY)

        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_multiple_files(self, oauth2_get_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["extra.evidence"] = [FILE_EVIDENCE_EMPTY, FILE_EVIDENCE_A]

        result = deepcopy(event)
        result["extra.fileinfo"] = [FILEINFO_EMPTY, FILEINFO_A]

        oauth2_get_mock.side_effect = Mock_API_Endpoint(
            "https://api.securitycenter.windows.com/api",
            {"files/da39a3ee5e6b4b0d3255bfef95601890afd80709": FILEINFO_EMPTY,
             "files/3f786850e387550fdab836ed7e6dc881de23001b": FILEINFO_A}
        )

        self.input_message = event
        self.run_bot()
        self.assertMessageEqual(0, result)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_missing_sha1(self, oauth2_get_mock, oauth2_fetch_token_mock):
        event = deepcopy(EVENT_BASE)
        event["extra.evidence"] = [FILE_EVIDENCE_EMPTY]

        result = deepcopy(event)
        result["extra.fileinfo"] = [FILEINFO_EMPTY]

        oauth2_get_mock.side_effect = Mock_API_Endpoint(
            "https://api.securitycenter.windows.com/api",
            {"files/da39a3ee5e6b4b0d3255bfef95601890afd80709": {"error": {"code": "NotFound"}},
             "files/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": FILEINFO_EMPTY}
        )

        self.input_message = event
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertRegexpMatchesLog(pattern=f"Error fetching file information for hash {event['extra.evidence'][0]['sha1']}: {{'code': 'NotFound'}}")
        self.assertMessageEqual(0, result)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
