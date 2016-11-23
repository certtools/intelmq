# -*- coding: utf-8 -*-

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class URLVirIPsParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            row = row.strip()
            if row == "" or row.startswith("#"):
                continue

            event = self.new_event(report)

            event.add('source.ip', row)

            event.add('classification.type', 'malware')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()


BOT = URLVirIPsParserBot
