# -*- coding: utf-8 -*-
""" IntelMQ parser for Netlab 360 data feeds. """

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime


class Netlab360ParserBot(ParserBot):
    DGA_FEED = {'http://data.netlab.360.com/feeds/dga/dga.txt'}
    MAGNITUDE_FEED = {'http://data.netlab.360.com/feeds/ek/magnitude.txt'}

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)

        else:
            value = line.split('\t')
            event = self.new_event(report)
            event.add('classification.identifier', value[0].lower())
            event.add('raw', line)

            if report['feed.url'] in Netlab360ParserBot.DGA_FEED:
                event.add('source.fqdn', value[1])
                event.add('time.source', value[3] + ' UTC')
                event.add('classification.type', 'c&c')
                event.add('event_description.url', 'http://data.netlab.360.com/dga')

            elif report['feed.url'] in Netlab360ParserBot.MAGNITUDE_FEED:
                event.add('time.source', DateTime.from_timestamp(int(value[1])))
                event.add('source.ip', value[2])
                event.add('source.fqdn', value[3])
                if value[4] != 'N/A':
                    event.add('source.url', value[4])
                event.add('classification.type', 'exploit')
                event.add('event_description.url', 'http://data.netlab.360.com/ek')
            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event

BOT = Netlab360ParserBot
