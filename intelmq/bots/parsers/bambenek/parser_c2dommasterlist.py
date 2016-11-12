# -*- coding: utf-8 -*-
"""
http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt
format:
ooxnererwyatanb.com,Domain used by banjori,2016-11-10 15:04,http://osint.bambenekconsulting.com/manual/banjori.txt
destination.fqdn,event_description.text,time.observation,event_description.url
"""

import sys
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

class Bambenekc2dommasterlistParserBot(Bot):

    def process(self):
        report = self.recieve_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():
            if row.startswith('#'):
                continue

            row_split = row.split(',')

            event = Event(report)

            event.add('destination.fqdn', row_split[0])
            event.add('event_description.text', row_split[1])
            event.add('time.observation', row_split[2])
            event.add('event_description.url', row_split[3])
            event.add('classification.type', 'c&c')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = Bambenekc2dommasterlistParserBot(sys.argv[1])
    bot.start()
