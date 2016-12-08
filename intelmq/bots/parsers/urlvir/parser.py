# -*- coding: utf-8 -*-
""" IntelMQ parser for URLVIR feeds """

import sys
import dateutil.parser

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import IPAddress
from intelmq.lib.message import Event


class URLVirParserBot(ParserBot):

    IP_FEED = {'http://www.urlvir.com/export-ip-addresses/'}
    HOST_FEED = {'http://www.urlvir.com/export-hosts/'}

    def parse_line(self, line, report):
        lastgenerated = None

        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
            if '#Updated on' in line:
                self.lastgenerated = line.strip('#Updated on ')
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated + ' -04:00').isoformat()

        else:
            event = Event(report)
            if report['feed.url'] in URLVirParserBot.IP_FEED:
                value = line.strip()
                if self.lastgenerated:
                    event.add('time.source', self.lastgenerated)
                event.add('source.ip', value)
                event.add('classification.type', 'malware')
                event.add('event_description.text', 'Active Malicious IP Addresses Hosting Malware')
                event.add('event_description.url', 'http://www.urlvir.com/search-ip-address/' + value + '/')
                event.add('raw', line)

            if report['feed.url'] in URLVirParserBot.HOST_FEED:
                value = line.strip()
                if self.lastgenerated:
                    event.add('time.source', self.lastgenerated)
                if IPAddress.is_valid(value):
                    event.add('source.ip', value)
                    event.add('event_description.url', 'http://www.urlvir.com/search-ip-address/' + value + '/')
                else:
                    event.add('source.fqdn', value)
                    event.add('event_description.url', 'http://www.urlvir.com/search-host/' + value + '/')
                event.add('classification.type', 'malware')
                event.add('event_description.text', 'Active Malicious Hosts')
                event.add('raw', line)

            yield event

BOT = URLVirParserBot
