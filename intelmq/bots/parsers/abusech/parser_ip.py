# -*- coding: utf-8 -*-
"""
Parsers simple newline separated list of IPs.

Docs:
 - https://feodotracker.abuse.ch/blocklist/
 - https://palevotracker.abuse.ch/blocklists.php
 - https://zeustracker.abuse.ch/blocklist.php
"""

import sys

import dateutil

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

SOURCE_FEEDS = {'https://feodotracker.abuse.ch/blocklist/?download=ipblocklist': 'Cridex',
                'https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist': 'Palevo',
                'https://zeustracker.abuse.ch/blocklist.php?download=badips': 'Zeus'}


class AbusechIPParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        lastgenerated = None

        for row in raw_report.splitlines():
            event = Event(report)

            row = row.strip()
            if len(row) == 0:
                continue
            elif row.startswith("#"):
                if 'Generated on' in row:
                    row = row.strip('# ')[13:]
                    lastgenerated = dateutil.parser.parse(row).isoformat()
                continue

            event.add('time.source', lastgenerated)

            event.add('source.ip', row)
            event.add('classification.type', 'c&c')
            event.add("raw", row)
            event.add("malware.name", SOURCE_FEEDS[report.get("feed.url")])

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AbusechIPParserBot(sys.argv[1])
    bot.start()
