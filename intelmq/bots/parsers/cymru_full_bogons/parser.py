# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime, IPAddress
from intelmq.lib.message import Event


class CymruFullBogonsParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()
            if row == "" or row[:2] == "//":
                continue

            event = Event()

            value = row.split(" ")[1]

            if IPAddress.is_valid(value, sanitize=True):
                event.add('source.ip', value, sanitize=True)
            else:
                event.add('source.network', value, sanitize=True)

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('classification.type', u'blacklist')
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('raw', row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = CymruFullBogonsParserBot(sys.argv[1])
    bot.start()
