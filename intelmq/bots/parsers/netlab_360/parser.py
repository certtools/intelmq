# -*- coding: utf-8 -*-
""" IntelMQ parser for Netlab 360 data feeds. """

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime


class Netlab360ParserBot(ParserBot):
    DGA_FEED = {'http://data.netlab.360.com/feeds/dga/dga.txt'}
    MAGNITUDE_FEED = {'http://data.netlab.360.com/feeds/ek/magnitude.txt'}
    MIRAI_SCANNER_FEED = {'http://data.netlab.360.com/feeds/mirai-scanner/scanner.list'}

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
                # DGA Feed format is
                # DGA family, Domian, Start and end of valid time(UTC)

                event.add('time.source', value[2] + ' UTC')
                if event['time.source'] > event['time.observation']:
                    event.change('time.source', event['time.observation'])
                event.add('classification.type', 'c&c')
                event.add('event_description.url', 'http://data.netlab.360.com/dga')

            elif report['feed.url'] in Netlab360ParserBot.MAGNITUDE_FEED:
                event.add('time.source', DateTime.from_timestamp(int(value[1])))
                event.add('source.ip', value[2])
                # ignore ips as fqdns
                event.add('source.fqdn', value[3], raise_failure=False)
                if value[4] != 'N/A':
                    event.add('source.url', value[4])
                event.add('classification.type', 'exploit')
                event.add('event_description.url', 'http://data.netlab.360.com/ek')
            elif report['feed.url'] in Netlab360ParserBot.MIRAI_SCANNER_FEED:
                event.add('time.source', value[0] + ' UTC')
                event.add('source.ip', value[1].replace('sip=', ''))
                event.add('destination.port', value[2].replace('dport=', ''))
                event.add('classification.type', 'scanner')
                event.add('classification.identifier', 'mirai', overwrite=True)
            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event


BOT = Netlab360ParserBot
