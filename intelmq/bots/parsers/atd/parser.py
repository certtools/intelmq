# -*- coding: utf-8 -*-
"""
ATDParserBot parses data from McAfee Advanced Threat Defense.

The following information is forwarded via queue:
IP
URL
Hash
"""
from __future__ import unicode_literals
import sys
import json

# imports for additional libraries and intelmq
import intelmq.lib.bot as Bot
import intelmq.lib.utils as utils


class ATDParserBot(Bot.ParserBot):

    SUPPORTED_ATD_SECTIONS = [
        'Processes',
        'Files',
        'Urls',
        'Ips',
    ]


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
        # print(atd_event['Summary']['Subject'])

        for section in atd_event['Summary']:
            if (section in self.SUPPORTED_ATD_SECTIONS):
                for entry in atd_event['Summary'][section]:
                    event = self.new_event(report)
                    for key, value in entry.items():
                        if (key in self.ATD_TYPE_MAPPING):
                            event.add(self.ATD_TYPE_MAPPING[key], value)
                    self.send_message(event)

        # event = self.new_event(report)  # copies feed.name, time.observation
        # implement the logic here

        # event.add('source.ip', '127.0.0.1')
        # event.add('extra', {"os.name": "Linux"})

        # self.send_message(event)
        self.acknowledge_message()

BOT = ATDParserBot
