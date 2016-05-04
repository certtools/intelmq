# -*- coding: utf-8 -*-
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class ArborParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.splitlines():
            row = row.strip()

            if len(row) == 0 or row.startswith('other'):
                continue

            event = Event(report)

            event.add('classification.type', 'brute-force')
            event.add("raw", row)

            columns = ["source.ip"]
            row = row.split()

            for key, value in zip(columns, row):
                event.add(key, value)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ArborParserBot(sys.argv[1])
    bot.start()
