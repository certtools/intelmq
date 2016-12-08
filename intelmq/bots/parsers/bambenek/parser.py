# -*- coding: utf-8 -*-
""" IntelMQ parser for Bambenek DGA, Domain, and IP feeds """

from intelmq.lib.bot import ParserBot


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
            event = self.new_event(report)

            event.add('source.ip', value[0])
            event.add('event_description.text', value[1])
            event.add('time.source', value[2] + ' UTC')
            event.add('event_description.url', value[3])

            if report['feed.url'] in BambenekParserBot.IPMASTERLIST or report['feed.url'] in BambenekParserBot.DOMMASTERLIST:
                event.add('classification.type', 'c&c')
                event.add('status', 'online')
                event.add('raw', line)

            elif report['feed.url'] in BambenekParserBot.DGA_FEED:
                event.add('classification.type', 'dga domain')
                event.add('raw', line)

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'] )

            yield event

BOT = BambenekParserBot
