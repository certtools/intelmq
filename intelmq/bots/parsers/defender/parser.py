# -*- coding: utf-8 -*-
"""Microsoft Defender API parser bot

Parses security alerts from Microsoft Defender ATP.

Defender wants to include quite a lot of information that doesn't fit
in IntelMQ's default harmonisation, so it abuses the "extra" namespace
to store its information.

Defender creates alerts of a number of different categories. The
dictionary category_map describes the routing of different categories
of alerts to different output queues. Alerts of a category not in any
mapping will be sent to the output queue specified as "invalid_path".

Output structure:

   "extra.defender_id": "Defender incident ID",
   "extra.evidence": [
      List of "evidence" structures. The format is fixed, but contains
      the union of all fields ever used. Hence, most fields are null,
      and which fields contain useful data depends on the type of
      evidence, which is stored in the "entityType" field.

      Structure:
      {
         "aadUserId": "",
         "accountName": "",
         "detectionStatus": "",
         "domainName": "",
         "entityType": "",
         "evidenceCreationTime": "Timestamp",
         "fileName": "",
         "filePath": "",
         "ipAddress": "",
         "parentProcessCreationTime": "",
         "parentProcessFileName": "",
         "parentProcessFilePath": "",
         "parentProcessId": "",
         "processCommandLine": "",
         "processCreationTime": "",
         "processId": "",
         "registryHive": "",
         "registryKey": "",
         "registryValue": "",
         "registryValueType": "",
         "sha1": "",
         "sha256": "",
         "url": "",
         "userPrincipalName": "",
         "userSid": ""
      }
   ]

   "extra.incident.status": "Defender's incident status",
   "extra.malware.category": "Malware category",
   "extra.malware.severity": "Malware severity",
   "extra.time.resolved": "Timestamp when Defender considered this incident resolved",
   "malware.name": "Malware name, if known",
   "source.fqdn": "Hostname of computer generating alert",
   "time.source": "Timestamp of the first event in this Defender incident"
   "source.account": "Account running the malware"
   "extra.machineid": "Defender ID of the machine running the malware"
   "extra.title": "Defender's title for this alert, somewhat suitable for use as ticket title"

SPDX-FileCopyrightText: 2021 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Parameters:

queue_map: map of strings to lists of strings, saying for each output
           queue which categories of alerts it receives. Matching is
           case insensitive. Multiple matches are allowed, and result
           in one copy of the alert getting sent to each matching
           output queue.
           Default:
           {
              "_default": [ "malware", "unwantedsoftware", "ransomware", "exploit", "credentialaccess" ]
           }

classification_map: map of strings to lists of strings, saying for
                    each IntelMQ classification which categories of
                    alerts get mapped to it. Alerts not matching any
                    entry are classified as "undetermined". Matching
                    is case insensitive.
                    Default:
                    {
                       "infected-system": ["malware", "unwantedsoftware", "ransomware"],
                       "exploit": ["exploit"],
                       "compromised": ["credentialaccess"],
                    }

invalid_path: string, default "invalid", the IntelMQ destination queue
              handling alerts with invalid categories.

"""
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.utils import base64_decode

import json
from typing import List, Dict


class DefenderParserBot(ParserBot):
    queue_map: Dict[str, List[str]] = {
        "_default": ["malware", "unwantedsoftware", "ransomware", "exploit", "credentialaccess"]
    }
    classification_map: Dict[str, List[str]] = {
        "infected-system": ["malware", "unwantedsoftware", "ransomware"],
        "exploit": ["exploit"],
        "compromised": ["credentialaccess"],
    }
    invalid_path: str = "invalid"

    @classmethod
    def add_if_present(self, report, out_field, struct, in_field):
        if struct.get(in_field, None) is not None:
            report.add(out_field, struct[in_field])

    @classmethod
    def format_timestamp(self, timestamp):
        return DateTime.convert_from_format(timestamp.split('.')[0] + "+0000", "%Y-%m-%dT%H:%M:%S%z")

    def process(self):
        report = self.receive_message()
        raw_report = base64_decode(report.get("raw"))
        alert = json.loads(raw_report)

        self.logger.debug("Considering alert: %s.", alert)
        event = self.new_event(report)
        event.add("raw", raw_report)

        category = alert.get("category", "unknown")
        output_queues = []
        for queue, categories in self.queue_map.items():
            for candidate_category in categories:
                if category.casefold() == candidate_category.casefold():
                    output_queues.append(queue)

        if output_queues == []:
            output_queues = [self.invalid_path]

        self.logger.debug("Category %s routed to paths %s.", category, output_queues)

        classification = "undetermined"
        for cf, categories in self.classification_map.items():
            for candidate_category in categories:
                if category.casefold() == candidate_category.casefold():
                    classification = cf
                    break

        self.logger.debug("Category %s assigned classification %s.", category, classification)
        event.add("classification.type", classification)

        if alert.get("relatedUser", None) and \
           alert["relatedUser"].get("userName", None):
            event.add("source.account", alert["relatedUser"]["userName"])

        self.add_if_present(event, "extra.defender_id", alert, "id")
        self.add_if_present(event, "source.fqdn", alert, "computerDnsName")
        self.add_if_present(event, "extra.malware.severity", alert, "severity")
        self.add_if_present(event, "malware.name", alert, "threatName")
        self.add_if_present(event, "extra.malware.category", alert, "category")
        self.add_if_present(event, "extra.incident.status", alert, "status")  # Check if failed?
        self.add_if_present(event, "extra.evidence", alert, "evidence")
        self.add_if_present(event, "extra.machineid", alert, "machineId")
        self.add_if_present(event, "extra.title", alert, "title")

        if alert.get("firstEventTime", None):
            event.add("time.source", self.format_timestamp(alert["firstEventTime"]))
        if alert.get("resolvedTime", None):
            event.add("extra.time.resolved", self.format_timestamp(alert["resolvedTime"]))

        for output_queue in output_queues:
            self.send_message(event, path=output_queue)
        self.acknowledge_message()


BOT = DefenderParserBot
