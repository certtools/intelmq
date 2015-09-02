# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from io import StringIO

import unicodecsv

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))

        columns = ["__IGNORE__",
                   "source.url",
                   "event_description.url",
                   "time.source",
                   "__IGNORE__",
                   "__IGNORE__",
                   "__IGNORE__",
                   "event_description.target"
                   ]

        for row in unicodecsv.reader(StringIO(raw_report), encoding='utf-8'):

            # ignore headers
            if "phish_id" in row:
                continue

            event = Event()

            for key, value in zip(columns, row):

                if key == "__IGNORE__":
                    continue

                event.add(key, value, sanitize=True)

            event.add('time.observation', report.value(
                'time.observation'), sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('classification.type', u'phishing')
            event.add("raw", ",".join(row), sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankParserBot(sys.argv[1])
    bot.start()
