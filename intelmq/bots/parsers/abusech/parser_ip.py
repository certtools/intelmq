# -*- coding: utf-8 -*-
"""
Parsers simple newline separated list of IPs.

Docs:
 - https://feodotracker.abuse.ch/blocklist/
 - https://palevotracker.abuse.ch/blocklists.php
"""
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

SOURCE_FEEDS = {'https://feodotracker.abuse.ch/blocklist/?download=ipblocklist': 'Cridex',
                'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist': 'Palevo',
                'https://zeustracker.abuse.ch/blocklist.php?download=badips': 'Zeus'}


class AbusechIPParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report:
            self.acknowledge_message()
            return
        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()

            if row.startswith("#") or len(row) == 0:
                continue

            event = Event(report)

            event.add('source.ip', row, sanitize=True)
            event.add('classification.type', u'c&c')
            event.add("raw", row, sanitize=True)
            event.add("malware.name", SOURCE_FEEDS[report.value("feed.url")], sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AbusechIPParserBot(sys.argv[1])
    bot.start()
