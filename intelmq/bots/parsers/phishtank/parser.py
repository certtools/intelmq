# -*- coding: utf-8 -*-
import csv
import io

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()

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
        raw_report = raw_report.translate({0: None})
        for row in csv.reader(io.StringIO(raw_report)):

            if not len(row):  # csv module can give empty lists
                self.acknowledge_message()
                return

            # ignore headers
            if "phish_id" in row:
                continue

            event = self.new_event(report)
            event.change("feed.url", event["feed.url"][:event["feed.url"].find('data/')])

            for key, value in zip(columns, row):

                if key == "__IGNORE__":
                    continue

                event.add(key, value)

            event.add('classification.type', 'phishing')
            event.add("raw", ",".join(row))

            self.send_message(event)
        self.acknowledge_message()


BOT = PhishTankParserBot
