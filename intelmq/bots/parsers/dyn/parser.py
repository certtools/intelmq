# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class DynParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.split('\n'):
            if row.startswith('#'):
                continue

            if (row.startswith("date started:") or
                    row.startswith("date finished:")):
                continue

            splitted_row = row.split("-->")
            if splitted_row[0] == '':
                continue

            infected_fqdn = splitted_row[0].split("checking domain:")[1]
            compromised_url = splitted_row[1].split("seems to be INFECTED:")[1]

            event_infected = Event(report)
            event_infected.add('classification.type', 'malware')
            event_infected.add('source.fqdn', infected_fqdn)
            event_infected.add('destination.url', compromised_url)
            event_infected.add('event_description.text',
                               'has malicious code redirecting to malicious '
                               'host')
            event_infected.add('raw', row)

            self.send_message(event_infected)

            event_compromised = Event(report)
            event_compromised.add('classification.type', 'compromised')
            event_compromised.add('source.url', compromised_url)
            event_compromised.add('event_description.text',
                                  'host has been compromised and has '
                                  'malicious code infecting users')
            event_compromised.add('raw', row)

            self.send_message(event_compromised)

        self.acknowledge_message()

if __name__ == "__main__":
    bot = DynParserBot(sys.argv[1])
    bot.start()
