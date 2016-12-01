# -*- coding: utf-8 -*-

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Event


class Netlab360ParserBot(ParserBot):
    DGA_FEED = {'http://data.netlab.360.com/feeds/dga/dga.txt'}
    MAGNITUDE_FEED = {'http://data.netlab.360.com/feeds/ek/magnitude.txt'}

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)

        else:
            value = line.split('\t')
            event = Event(report)

            if report['feed.url'] in Netlab360ParserBot.DGA_FEED:
                event.add('classification.identifier', value[0].lower())
                event.add('source.fqdn', value[1])
                event.add('time.source', value[3] + ' UTC')
                event.add('raw', line)
                event.add('classification.type', 'c&c')
                event.add('event_description.url', 'http://data.netlab.360.com/dga')

            if report['feed.url'] in Netlab360ParserBot.MAGNITUDE_FEED:
                event.add('classification.identifier', value[0].lower())
                event.add('time.source', DateTime.from_timestamp(int(value[1])))
                event.add('source.ip', value[2])
                event.add('source.fqdn', value[3])
                if value[4] != 'N/A':
                    event.add('source.url', value[4])
                event.add('raw', line)
                event.add('classification.type', 'exploit')
                event.add('event_description.url', 'http://data.netlab.360.com/ek')

            yield event

if __name__ == '__main__':
    bot = Netlab360ParserBot(sys.argv[1])
    bot.start()
