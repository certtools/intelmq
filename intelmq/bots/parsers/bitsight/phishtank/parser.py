# -*- coding: utf-8 -*-
import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        columns = ["__IGNORE__",
                   "source.url",
                   "event_description.url",
                   "time.source",
                   "__IGNORE__",
                   "__IGNORE__",
                   "__IGNORE__",
                   "event_description.target"
                   ]

        raw_report = utils.base64_decode(report.get("raw"))
        for row in csv.reader(io.StringIO(raw_report)):

            # ignore headers
            if "phish_id" in row:
                continue

            event = Event(report)

            for key, value in zip(columns, row):

                if key == "__IGNORE__":
                    continue

                event.add(key, value)

            event.add('classification.type', u'phishing')
            event.add("raw", ",".join(row))

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankParserBot(sys.argv[1])
    bot.start()
