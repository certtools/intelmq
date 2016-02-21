# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class TurrisGreylistParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        columns = [
            "source.ip",
            "__IGNORE__",
            "event_description.text",
            "__IGNORE__"
        ]

        headers = True
        raw_report = utils.base64_decode(report.get("raw"))
        for row in utils.csv_reader(raw_report):
            # ignore headers
            if headers:
                headers = False
                continue

            event = Event(report)

            for key, value in zip(columns, row):
                if key == "__IGNORE__":
                    continue

                event.add(key, value)

            event.add('classification.type', u'scanner')
            event.add("raw", ",".join(row))

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = TurrisGreylistParserBot(sys.argv[1])
    bot.start()
