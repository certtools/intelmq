# -*- coding: utf-8 -*-

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class HpHostsParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():
            row = row.strip()

            if len(row) == 0 or row.startswith('#'):
                continue

            row = row.replace('\r', '')
            values = row.split('\t')

            # if special char is in string should not be allowed
            if "#" in values[1]:
                continue

            # if domain name is localhost we are not interested
            if values[1].lower().strip() == "localhost":
                continue

            event = self.new_event(report)

            if not event.add("source.ip", values[1], raise_failure=False):
                event.add("source.fqdn", values[1])

            event.add('classification.type', 'blacklist')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = HpHostsParserBot
