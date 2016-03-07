# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress
from intelmq.lib.message import Event


class HpHostsParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if (report is None or not report.contains("raw") or
                len(report.get("raw").strip()) == 0):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.split('\n'):
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

            event = Event(report)

            if IPAddress.is_valid(values[1]):
                event.add("source.ip", values[1])
            else:
                event.add("source.fqdn", values[1])

            event.add('classification.type', u'blacklist')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = HpHostsParserBot(sys.argv[1])
    bot.start()
