# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import unittest
from copy import deepcopy

import intelmq.lib.test as test
from intelmq.lib.utils import base64_encode
from intelmq.bots.parsers.defender.parser import DefenderParserBot

ALERT_BASE = {
    "id": "abc123-456789",
    "title": "'Example' malware detected",
    "incidentId": 12345,
    "assignedTo": None,
    "status": "Test",
    "classification": None,
    "alertCreationTime": "2021-05-25T01:01:01.1234567Z",
    "firstEventTime": "2021-05-25T02:02:02.1234567Z",
    "lastEventTime": "2021-05-25T03:03:03.1234567Z",
    "lastUpdateTime": "2021-05-25T04:04:04.1234567Z",
    "resolvedTime": None,
    "computerDnsName": "test.example.com",
    "evidence": []
}

EVENT_BASE = {
    'feed.url': 'https://api.securitycenter.windows.com/api',
    'feed.name': 'Defender parser test',
    '__type': 'Event',
    'time.observation': '2021-05-25T06:06:06+00:00'
}

REPORT_BASE = {
    'feed.url': 'https://api.securitycenter.windows.com/api',
    'feed.name': 'Defender parser test',
    '__type': 'Report',
    'time.observation': '2021-05-25T06:06:06+00:00'
}

RELATED_USER = {
    "userName": "test123",
    "domainName": "example"
}

FILE_EVIDENCE = {
    "entityType": "File",
    "evidenceCreationTime": "2021-05-25T05:05:05.1234567Z",
    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",  # The empty string
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "fileName": "eicar.com",
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


class TestDefenderParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DefenderParserBot

    def test_full_alert(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "Malware"

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "infected-system"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "Malware"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["extra.title"] = "'Example' malware detected"
        event["extra.evidence"] = []

        self.input_message = report
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_user(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "Malware"
        alert["relatedUser"] = RELATED_USER

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "infected-system"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "Malware"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["source.account"] = "test123"
        event["extra.title"] = "'Example' malware detected"
        event["extra.evidence"] = []

        self.input_message = report
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_invalid_category(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "TestCategory"

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "undetermined"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "TestCategory"
        event["extra.title"] = "'Example' malware detected"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["extra.evidence"] = []

        self.input_message = report
        self.prepare_bot(destination_queues={
            "_default": "default_output_queue",
            "invalid": "invalid_queue"
        })
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0, "_default")
        self.assertOutputQueueLen(1, "invalid")
        self.assertMessageEqual(0, event, path="invalid")

    def test_file_evidence(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "Malware"
        alert["evidence"] = [FILE_EVIDENCE]

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "infected-system"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "Malware"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["extra.evidence"] = [FILE_EVIDENCE]
        event["extra.title"] = "'Example' malware detected"

        self.input_message = report
        self.run_bot()
        self.assertMessageEqual(0, event)

    def test_custom_classification(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "TestCategory"

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "application-compromise"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "TestCategory"
        event["extra.title"] = "'Example' malware detected"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["extra.evidence"] = []

        self.input_message = report
        self.prepare_bot(parameters={
            "queue_map": {
                "_default": ["TestCategory"]
            },
            "classification_map": {
                "application-compromise": ["TestCategory"]
            }})
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(1, "_default")
        self.assertMessageEqual(0, event, path="_default")

    def test_custom_routing(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "TestCategory"

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "undetermined"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "TestCategory"
        event["extra.title"] = "'Example' malware detected"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["extra.evidence"] = []

        self.input_message = report
        self.prepare_bot(
            parameters={
                "queue_map": {
                    "_default": ["malware"],
                    "test": ["TestCategory"]
                }
            },
            destination_queues={
                "_default": "default-output-queue",
                "test": "test-queue"
            }
        )
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0, "_default")
        self.assertOutputQueueLen(1, "test")
        self.assertMessageEqual(0, event, path="test")

    def test_multiple_routes(self):
        alert = deepcopy(ALERT_BASE)
        alert["category"] = "TestCategory"

        report = deepcopy(REPORT_BASE)
        report["raw"] = base64_encode(json.dumps(alert))

        event = deepcopy(EVENT_BASE)
        event["raw"] = report["raw"]
        event["classification.type"] = "undetermined"
        event["extra.defender_id"] = "abc123-456789"
        event["extra.incident.status"] = "Test"
        event["extra.malware.category"] = "TestCategory"
        event["extra.title"] = "'Example' malware detected"
        event["source.fqdn"] = "test.example.com"
        event["time.source"] = "2021-05-25T02:02:02+00:00"
        event["extra.evidence"] = []

        self.input_message = report
        self.prepare_bot(
            parameters={
                "queue_map": {
                    "_default": ["malware"],
                    "test": ["TestCategory"],
                    "test2": ["TestCategory"]
                }
            },
            destination_queues={
                "_default": "default-output-queue",
                "test": "test-queue",
                "test2": "test-queue-2"
            }
        )
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0, "_default")
        self.assertOutputQueueLen(1, "test")
        self.assertOutputQueueLen(1, "test2")
        self.assertMessageEqual(0, event, path="test")
        self.assertMessageEqual(0, event, path="test2")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
