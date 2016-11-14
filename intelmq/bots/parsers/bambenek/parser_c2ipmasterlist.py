# -*- coding: utf-8 -*-
"""
http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt
format:
31.170.178.179,IP used by beebone C&C,2016-11-12 14:09,http://osint.bambenekconsulting.com/manual/beebone.txt
destination.ip,event_description.text,time.source,event_description.url
"""

import sys
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class Bambenekc2ipmasterlistParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():
            if row.startswith('#'):
                continue

            row_split = row.split(',')

            event = Event(report)

            event.add('destination.ip', row_split[0])
            event.add('event_description.text', row_split[1])
            event.add('time.source', row_split[2] + " UTC")
            event.add('event_description.url', row_split[3])
            event.add('classification.type', 'c&c')
            event.add('status', 'online')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = Bambenekc2ipmasterlistParserBot(sys.argv[1])
    bot.start()
