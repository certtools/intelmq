# -*- coding: utf-8 -*-
"""

ATDFileParserBot parses file information from McAfee Advanced Threat Defense reports.

Parameter:
verdict_severity: defines the minimum severity of reports to be parsed
                  severity ranges from 1 to 5
"""
from __future__ import unicode_literals
import sys
import json

# imports for additional libraries and intelmq
import intelmq.lib.bot as Bot
import intelmq.lib.utils as utils


class ATDFileParserBot(Bot.ParserBot):

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
            # forward initial sample
            event = self.new_event(report)
            event.add('malware.name', subject_name)
            event.add('malware.hash.md5', subject_md5)
            event.add('malware.hash.sha1', subject_sha1)
            event.add('malware.hash.sha256', subject_sha256)
            self.send_message(event)

            # forward any subsequent files (dropped payload, if any)
            try:
                for entry in atd_event['Summary']['Files']:
                    event = self.new_event(report)
                    for key, value in entry.items():
                        if (key in self.ATD_TYPE_MAPPING):
                            event.add(self.ATD_TYPE_MAPPING[key], value)
                    self.send_message(event)
            except KeyError:
                pass

        self.acknowledge_message()

BOT = ATDFileParserBot
