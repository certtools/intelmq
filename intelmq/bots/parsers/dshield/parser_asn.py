# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class DShieldASNParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):

            if row.startswith('#'):
                continue

            values = row.split("\t")

            if len(values) < 6:
                continue    # raise an error

            source_ip = values[0]
            reports = values[1]
            targets = values[2]
            first_seen = values[3]
            last_seen = values[4] + 'T00:00:00+00:00'
            updated = values[5]

            parts = source_ip.split(".")
            part_index = 0
            for part in parts:
                parts[part_index] = str(int(part))
                part_index += 1

            source_ip = ".".join(parts)

            event = Event()

            event.add('source.ip', source_ip, sanitize=True)
            event.add('classification.type', u'brute-force')
            event.add('time.observation', report.value(
                'time.observation'), sanitize=True)
            event.add("time.source", last_seen, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DShieldASNParserBot(sys.argv[1])
    bot.start()
