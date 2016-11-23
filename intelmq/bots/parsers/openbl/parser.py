# -*- coding: utf-8 -*-
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class OpenBLParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.splitlines():

            row = row.strip()

            if len(row) == 0 or row.startswith('#'):
                continue

            splitted_row = row.split()
            event = self.new_event(report)

            columns = ["source.ip", "time.source"]

            for key, value in zip(columns, splitted_row):
                if key == "time.source":
                    value = datetime.utcfromtimestamp(
                        int(value)).strftime('%Y-%m-%d %H:%M:%S') + " UTC"

                event.add(key, value.strip())

            event.add('classification.type', 'blacklist')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = OpenBLParserBot
