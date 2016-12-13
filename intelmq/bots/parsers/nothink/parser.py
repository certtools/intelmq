# -*- coding: utf-8 -*-
""" IntelMQ parser for Nothink feeds """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class NothinkParserBot(ParserBot):
    lastgenerated = None

    SOURCE_FEEDS = {'http://www.nothink.org/blacklist/blacklist_snmp_day.txt': 'snmp',
                    'http://www.nothink.org/blacklist/blacklist_snmp_week.txt': 'snmp',
                    'http://www.nothink.org/blacklist/blacklist_snmp_year.txt': 'snmp',
                    'http://www.nothink.org/blacklist/blacklist_ssh_day.txt': 'ssh',
                    'http://www.nothink.org/blacklist/blacklist_ssh_week.txt': 'ssh',
                    'http://www.nothink.org/blacklist/blacklist_ssh_year.txt': 'ssh',
                    'http://www.nothink.org/blacklist/blacklist_telnet_day.txt': 'telnet',
                    'http://www.nothink.org/blacklist/blacklist_telnet_week.txt': 'telnet',
                    'http://www.nothink.org/blacklist/blacklist_telnet_year.txt': 'telnet',
                    'http://www.nothink.org/honeypot_dns_attacks.txt': 'dns'
                    }

    BLACKLIST_FEED = {'http://www.nothink.org/blacklist/blacklist_snmp_day.txt',
                      'http://www.nothink.org/blacklist/blacklist_snmp_week.txt',
                      'http://www.nothink.org/blacklist/blacklist_snmp_year.txt',
                      'http://www.nothink.org/blacklist/blacklist_ssh_day.txt',
                      'http://www.nothink.org/blacklist/blacklist_ssh_week.txt',
                      'http://www.nothink.org/blacklist/blacklist_ssh_year.txt',
                      'http://www.nothink.org/blacklist/blacklist_telnet_day.txt',
                      'http://www.nothink.org/blacklist/blacklist_telnet_week.txt',
                      'http://www.nothink.org/blacklist/blacklist_telnet_year.txt'
                      }

    DNS_FEED = {'http://www.nothink.org/honeypot_dns_attacks.txt'}

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
            if 'Generated' in line:
                self.lastgenerated = line.strip('# Generated ')[:19]
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated + '+00:00').isoformat()

        else:
            event = self.new_event(report)
            event.add('raw', line)
            if report['feed.url'] in NothinkParserBot.BLACKLIST_FEED:
                event.add('time.source', self.lastgenerated)
                event.add('source.ip', line)
                event.add('classification.type', 'scanner')
                event.add('protocol.application', NothinkParserBot.SOURCE_FEEDS[report['feed.url']])

            elif report['feed.url'] in NothinkParserBot.DNS_FEED:
                value = line.strip('"').split('","')
                event.add('time.source', dateutil.parser.parse(value[0] + '+00:00').isoformat())
                event.add('source.ip', value[1])
                event.add('source.asn', value[2])
                event.add('source.as_name', value[3])
                if value[4] not in ['.', 'n/a', 'bka']:
                    event.add('source.reverse_dns', value[4])
                if value[5] != 'UNK':
                    event.add('source.geolocation.cc', value[5])
                event.add('protocol.application', NothinkParserBot.SOURCE_FEEDS[report['feed.url']])
                event.add('classification.type', 'ddos')
                event.add('event_description.text', 'On time.source the source.ip was seen'
                                                    ' performing DNS amplification attacks against honeypots')

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event

BOT = NothinkParserBot
