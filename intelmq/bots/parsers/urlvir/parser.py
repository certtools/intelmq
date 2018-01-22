# -*- coding: utf-8 -*-
""" IntelMQ parser for URLVIR feeds """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class URLVirParserBot(ParserBot):

    IP_FEED = {'http://www.urlvir.com/export-ip-addresses/'}
    HOST_FEED = {'http://www.urlvir.com/export-hosts/'}

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
            if '#Updated on' in line:
                self.lastgenerated = line.strip('#Updated on ')
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated + ' -04:00').isoformat()

        else:
            event = self.new_event(report)
            value = line.strip()
            if self.lastgenerated:
                event.add('time.source', self.lastgenerated)
            event.add('raw', line)
            event.add('classification.type', 'malware')

            if report['feed.url'] in URLVirParserBot.IP_FEED:
                event.add('source.ip', value)
                event.add('event_description.text', 'Active Malicious IP Addresses Hosting Malware')
                event.add('event_description.url', 'http://www.urlvir.com/search-ip-address/' + value + '/')

            elif report['feed.url'] in URLVirParserBot.HOST_FEED:
                if event.is_valid('source.ip', value):
                    event.add('source.ip', value)
                    event.add('event_description.url', 'http://www.urlvir.com/search-ip-address/' + value + '/')
                else:
                    event.add('source.fqdn', value)
                    event.add('event_description.url', 'http://www.urlvir.com/search-host/' + value + '/')
                event.add('event_description.text', 'Active Malicious Hosts')

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event


BOT = URLVirParserBot
