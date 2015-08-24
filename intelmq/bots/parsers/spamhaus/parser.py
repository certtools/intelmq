# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Event


class SpamHausParserBot(Bot):

    def process(self):
        report = self.receive_message()
        self.event_date = None

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()

            if row.startswith('; Last-Modified:'):
                self.event_date = row.split('; Last-Modified: ')[1].strip()
                self.event_date = datetime.strptime(self.event_date,
                                                    "%a, %d %b %Y %H:%M:%S %Z")

            if row == "" or row.startswith(';'):
                continue

            row_splitted = row.split(';')
            network = row_splitted[0].strip()

            event = Event()

            event.add('source.network', network, sanitize=True)
            if self.event_date:
                event.add('time.source', self.event_date, sanitize=True)

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('classification.type', u'spam')
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('raw', row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = SpamHausParserBot(sys.argv[1])
    bot.start()
