# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class OpenBLParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.split('\n'):

            row = row.strip()

            if len(row) == 0 or row.startswith('#'):
                continue

            splitted_row = row.split()
            event = Event(report)

            columns = ["source.ip", "time.source"]

            for key, value in zip(columns, splitted_row):
                if key == "time.source":
                    value = datetime.utcfromtimestamp(
                        int(value)).strftime('%Y-%m-%d %H:%M:%S') + " UTC"

                event.add(key, value.strip())

            event.add('classification.type', u'blacklist')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = OpenBLParserBot(sys.argv[1])
    bot.start()
