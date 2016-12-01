# -*- coding: utf-8 -*-
""" IntelMQ parser for Bambenek DGA, Domain, and IP feeds """

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class BambenekParserBot(ParserBot):
    """ Single parser for Bambenek feeds """

    IPMASTERLIST = {'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt'}
    DOMMASTERLIST = {'http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt'}
    DGA_FEED = {'http://osint.bambenekconsulting.com/feeds/dga-feed.txt'}

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)

        else:
            value = line.split(',')
            event = Event(report)

            if report['feed.url'] in BambenekParserBot.IPMASTERLIST:
                event.add('source.ip', value[0])
                event.add('event_description.text', value[1])
                event.add('time.source', value[2] + ' UTC')
                event.add('event_description.url', value[3])
                event.add('classification.type', 'c&c')
                event.add('status', 'online')
                event.add('raw', line)

            if report['feed.url'] in BambenekParserBot.DOMMASTERLIST:
                event.add('source.fqdn', value[0])
                event.add('event_description.text', value[1])
                event.add('time.source', value[2] + ' UTC')
                event.add('event_description.url', value[3])
                event.add('classification.type', 'c&c')
                event.add('status', 'online')
                event.add('raw', line)

            if report['feed.url'] in BambenekParserBot.DGA_FEED:
                event.add('source.fqdn', value[0])
                event.add('event_description.text', value[1])
                event.add('time.source', value[2] + ' 00:00 UTC')
                event.add('event_description.url', value[3])
                event.add('classification.type', 'dga domain')
                event.add('raw', line)

            yield event

if __name__ == '__main__':
    bot = BambenekParserBot(sys.argv[1])
    bot.start()
