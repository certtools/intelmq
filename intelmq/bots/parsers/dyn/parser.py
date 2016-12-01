# -*- coding: utf-8 -*-
"""
format:
ponmocup-malware-IP ponmocup-malware-domain ponmocup-malware-URI-path ponmocup-htaccess-infected-domain
"""


import dateutil.parser

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class DynParserBot(Bot):

    def init(self):
        self.TZOFFSETS = {'PST': -8 * 60 * 60,
                          'PDT': -7 * 60 * 60}

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))
        source_time = None

        for row in raw_report.splitlines():
            if row.startswith("# last updated:"):
                source_time = dateutil.parser.parse(row[row.find(':') + 1:],
                                                    tzinfos=self.TZOFFSETS)
                source_time = source_time.isoformat()
                continue
            if row.startswith('#'):
                continue

            row_split = row.split()

            event_infected = self.new_event(report)
            event_infected.add('time.source', source_time)
            event_infected.add('classification.type', 'malware')
            if row_split[0] != '/':
                event_infected.add('source.ip', row_split[0])
            event_infected.add('source.fqdn', row_split[1])
            event_infected.add('source.url', row_split[2])
            event_infected.add('destination.fqdn', row_split[3])
            event_infected.add('event_description.text',
                               'has malicious code redirecting to malicious '
                               'host')
            event_infected.add('raw', row)

            self.send_message(event_infected)

            event_compromised = self.new_event(report)
            event_compromised.add('time.source', source_time)
            event_compromised.add('classification.type', 'compromised')
            if row_split[0] != '/':
                event_compromised.add('destination.ip', row_split[0])
            event_compromised.add('destination.fqdn', row_split[1])
            event_compromised.add('destination.url', row_split[2])
            event_compromised.add('source.fqdn', row_split[3])
            event_compromised.add('event_description.text',
                                  'host has been compromised and has '
                                  'malicious code infecting users')
            event_compromised.add('raw', row)

            self.send_message(event_compromised)

        self.acknowledge_message()


BOT = DynParserBot
