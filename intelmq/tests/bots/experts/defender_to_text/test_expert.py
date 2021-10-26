# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest
from copy import deepcopy
import json

import intelmq.lib.test as test
from intelmq.lib.utils import base64_encode
from intelmq.bots.experts.defender_to_text.expert import DefenderToTextExpertBot

ALERT = {
    'id': 'da161714175830432893_25502852604',
    'incidentId': 4311,
    'investigationId': 6428,
    'assignedTo': 'user@example.com',
    'severity': 'Medium',
    'status': 'InProgress',
    'classification': 'Unknown',
    'determination': 'Apt',
    'investigationState': 'PartiallyRemediated',
    'detectionSource': 'CustomerTI',
    'detectorId': 'c6c31072-b9c2-4f31-bcd2-4d3df408d9e3',
    'category': 'Exploit',
    'threatFamilyName': 'IntelMQ_Test_Alert',
    'title': 'IntelMQ test alert',
    'description': 'This is a IntelMQ test alert',
    'alertCreationTime': '2021-06-17T09:56:40.7545370Z',
    'firstEventTime': '2021-06-17T09:56:40.7546160Z',
    'lastEventTime': '2021-06-17T09:56:40.7546380Z',
    'lastUpdateTime': '2021-06-17T09:56:40.7546530Z',
    'resolvedTime': '2021-06-17T09:56:40.7546660Z',
    'machineId': '1d6c5feebe17192eef30c4b1d67ec32cd2b7db8c',
    'computerDnsName': 'computer.example.com',
    'rbacGroupName': None,
    'aadTenantId': '7fcc24e1-9156-4023-badc-c45b0f33011b',
    'threatName': 'IntelMQ:Test_Alert',
    'relatedUser': [],
    'comments': [],
    'evidence': [
        {
            'entityType': 'Url',
            'evidenceCreationTime': '2021-06-17T09:56:40.7546160Z',
            'sha1': None,
            'sha256': None,
            'fileName': None,
            'filePath': None,
            'processId': None,
            'processCommandLine': None,
            'processCreationTime': None,
            'parentProcessId': None,
            'parentProcessCreationTime': None,
            'parentProcessFileName': None,
            'parentProcessFilePath': None,
            'ipAddress': None,
            'url': 'https://www.example.com/test',
            'registryKey': None,
            'registryHive': None,
            'registryValueType': None,
            'registryValue': None,
            'accountName': None,
            'domainName': None,
            'userSid': None,
            'aadUserId': None,
            'userPrincipalName': None,
            'detectionStatus': None
        }
    ]
}

EVENT = {
    "feed.url": "https://api.securitycenter.windows.com/api",
    "feed.name": "Defender to text test",
    "__type": "Event",
    "raw": base64_encode(json.dumps(ALERT))
}


class TestDefenderToTextExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DefenderToTextExpertBot
        cls.sysconfig = {}

    def test_event(self):
        self.input_message = EVENT
        output = deepcopy(EVENT)
        output["output"] = json.dumps(ALERT, indent=4)
        self.run_bot()
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, output)

    def test_malformed(self):
        event = deepcopy(EVENT)
        not_json = "The quick brown fox jumps over the lazy dog."
        event["raw"] = base64_encode(not_json)
        self.input_message = event
        output = deepcopy(event)
        output["output"] = json.dumps(not_json)
        self.allowed_error_count = 1
        self.run_bot()
        self.assertLogMatches(pattern="JSON error loading alert:", levelname="ERROR")
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, output)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
