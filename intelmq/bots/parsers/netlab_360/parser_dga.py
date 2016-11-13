# -*- coding: utf-8 -*-
"""
feed:
http://data.netlab.360.com/feeds/dga/dga.txt
format:
suppobox        difficultdress.net      2016-11-12 11:58:56     2016-11-13 00:04:15
reference:
http://data.netlab.360.com/dga
"""

import sys
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

class Netlab360DGAParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():
            if row.startswith('#') or len(row) == 0:
                continue

            row_split = row.split('\t')

            event = Event(report)

            event.add('classification.identifier', row_split[0].lower())
            event.add('time.source', row_split[3] + " UTC")
            event.add('destination.fqdn', row_split[1])
            event.add('raw', row)
            event.add('classification.type', 'malware')
            event.add('event_description.url', 'http://data.netlab.360.com/dga')

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = Netlab360DGAParserBot(sys.argv[1])
    bot.start()
