# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class AbusechDomainParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()

            if row.startswith("#") or len(row) == 0:
                continue

            event = Event()

            event.add('classification.type', u'c&c')
            event.add('source.fqdn', row, sanitize=True)
            event.add('time.observation', report.value(
                'time.observation'), sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = AbusechDomainParserBot(sys.argv[1])
    bot.start()
