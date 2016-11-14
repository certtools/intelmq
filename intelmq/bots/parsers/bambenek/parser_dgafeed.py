# -*- coding: utf-8 -*-
"""
feed:
http://osint.bambenekconsulting.com/feeds/dga-feed.txt
format:
xqmclnusaswvof.com,Domain used by Cryptolocker - Flashback DGA for 10 Nov 2016,2016-11-10,
http://osint.bambenekconsulting.com/manual/cl.txt
destination.fqdn,event_description.text,time.source,event_description.url
"""

import sys
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

class BambenekDGAfeedParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():
            if row.startswith('#'):
                continue

            row_split = row.split(',')

            event = Event(report)

            event.add('destination.fqdn', row_split[0])
            event.add('event_description.text', row_split[1])
            event.add('time.source', row_split[2] + " 00:00 UTC")
            event.add('event_description.url', row_split[3])
            event.add('classification.type', 'ransomware')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = BambenekDGAfeedParserBot(sys.argv[1])
    bot.start()
