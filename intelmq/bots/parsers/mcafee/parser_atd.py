# -*- coding: utf-8 -*-
"""
ATDParserBot parses McAfee Advanced Threat Defense reports.
This bot generates one message per identified IOC:
- hash values of original sample and any identified dropped file
- IP addresses the sample tries to connect to
- FQDNs the sample tries to connect to

Parameter:
verdict_severity: defines the minimum severity of reports to be parsed
                  severity ranges from 1 to 5

"""
import json

import intelmq.lib.utils as utils
# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot


class ATDParserBot(Bot):

    ATD_TYPE_MAPPING = {
        'domain': 'source.fqdn',
        'hostname': 'source.fqdn',
        'Name': 'malware.name',
        'Md5': 'malware.hash.md5',
        'Sha1': 'malware.hash.sha1',
        'Sha256': 'malware.hash.sha256',
        'Ipv4': 'destination.ip',
        'Port': 'destination.port',
        'Url': 'destination.fqdn',
    }

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get('raw'))
        atd_event = json.loads(raw_report)

        subject_name = atd_event['Summary']['Subject']['Name']
        subject_md5 = atd_event['Summary']['Subject']['md5']
        subject_sha1 = atd_event['Summary']['Subject']['sha-1']
        subject_sha256 = atd_event['Summary']['Subject']['sha-256']
        verdict_severity = int(atd_event['Summary']['Verdict']['Severity'])

        if (verdict_severity >= int(self.parameters.verdict_severity)):

            # forward initial sample hashes
            event = self.new_event(report)
            event.add("classification.taxonomy", "malicious code")
            event.add("classification.type", 'infected-system')
            event.add("raw", raw_report)

            event.add('malware.name', subject_name)
            event.add('malware.hash.md5', subject_md5)
            event.add('malware.hash.sha1', subject_sha1)
            event.add('malware.hash.sha256', subject_sha256)

            self.send_message(event)

            # forward subsequent file hashes (dropped payload, if any)
            try:
                for entry in atd_event['Summary']['Files']:
                    event = self.new_event(report)
                    event.add("classification.taxonomy", "malicious code")
                    event.add("classification.type", 'infected-system')
                    event.add("raw", raw_report)
                    for key, value in entry.items():
                        if (key in self.ATD_TYPE_MAPPING):
                            event.add(self.ATD_TYPE_MAPPING[key], value)
                    self.send_message(event)
            except KeyError:
                pass

            # forward identified IP addresses, if any
            try:
                for entry in atd_event['Summary']['Ips']:
                    event = self.new_event(report)
                    event.add("classification.taxonomy", "malicious code")
                    event.add("classification.type", 'infected-system')
                    event.add("raw", raw_report)

                    event.add('malware.name', subject_name)
                    event.add('malware.hash.md5', subject_md5)
                    event.add('malware.hash.sha1', subject_sha1)
                    event.add('malware.hash.sha256', subject_sha256)

                    for key, value in entry.items():
                        if (key in self.ATD_TYPE_MAPPING):
                            event.add(self.ATD_TYPE_MAPPING[key], value)

                    self.send_message(event)
            except KeyError:
                pass

            # forward identified FQDNs, if any
            try:
                for entry in atd_event['Summary']['Urls']:
                    event = self.new_event(report)
                    event.add("classification.taxonomy", "malicious code")
                    event.add("classification.type", 'infected-system')
                    event.add("raw", raw_report)

                    event.add('malware.name', subject_name)
                    event.add('malware.hash.md5', subject_md5)
                    event.add('malware.hash.sha1', subject_sha1)
                    event.add('malware.hash.sha256', subject_sha256)

                    for key, value in entry.items():
                        if (key in self.ATD_TYPE_MAPPING):
                            event.add(self.ATD_TYPE_MAPPING[key], value)
                    self.send_message(event)
            except KeyError:
                pass

        self.acknowledge_message()


BOT = ATDParserBot
