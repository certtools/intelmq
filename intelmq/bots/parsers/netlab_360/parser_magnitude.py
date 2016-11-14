# -*- coding: utf-8 -*-
"""
feed:
http://data.netlab.360.com/feeds/ek/magnitude.txt
format:
Magnitude	1478939365	178.32.227.12	f57idayaa1.notsite.faith	http://f57idayaa1.notsite.faith/1c472e11922f6a0a6c20fa5996aa35f4
Magnitude	1478907804	178.32.227.12	3w212q83hay0ao51fi.courtall.party	N/A
reference:
http://data.netlab.360.com/ek
"""

import sys
from datetime import datetime
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class Netlab360MagnitudeParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():
            if row.startswith('#') or len(row) == 0:
                continue

            row_split = row.split('\t')

            event = Event(report)

            event.add('classification.identifier', row_split[0].lower())
            event.add('time.source', datetime.utcfromtimestamp(int(row_split[1])).strftime('%Y-%m-%dT%H:%M:%S+00:00'))
            event.add('destination.ip', row_split[2])
            event.add('destination.fqdn', row_split[3])
            event.add('destination.url', row_split[4])
            event.add('raw', row)
            event.add('classification.type', 'exploit')
            event.add('event_description.url', 'http://data.netlab.360.com/ek')

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = Netlab360MagnitudeParserBot(sys.argv[1])
    bot.start()
