# -*- coding: utf-8 -*-
""" Single IntelMQ parser for Spamhaus drop feeds """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class SpamhausDropParserBot(ParserBot):
    """ Spamhaus Drop Parser Bot """

    NETWORK_DROP_URLS = {'https://www.spamhaus.org/drop/edrop.txt',
                         'https://www.spamhaus.org/drop/dropv6.txt',
                         'https://www.spamhaus.org/drop/drop.txt',
                         'https://www.spamhaus.org/drop/drop.lasso'}

    ASN_DROP_URLS = {'https://www.spamhaus.org/drop/asndrop.txt'}
    lastgenerated = None

    def parse_line(self, line, report):

        if line.startswith(';') or len(line) == 0:
            self.tempdata.append(line)
            if 'Last-Modified:' in line:
                self.lastgenerated = line.strip('; ')[15:]
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated).isoformat()

        else:
            event = self.new_event(report)
            if self.lastgenerated:
                event.add('time.source', self.lastgenerated)
            event.add('classification.type', 'spam')
            event.add('raw', line)

            if report['feed.url'] in SpamhausDropParserBot.NETWORK_DROP_URLS:
                value = line.strip().split(';')
                event.add('source.network', value[0].strip())
                event.add('extra', {'blocklist': value[1].strip()})

            elif report['feed.url'] in SpamhausDropParserBot.ASN_DROP_URLS:
                value = line.replace('|', ';').split(';')
                event.add('source.asn', value[0].strip('AS').strip())
                event.add('source.as_name', value[2].strip())
                if value[1] != '':
                    event.add('source.geolocation.cc', value[1].strip())

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event


BOT = SpamhausDropParserBot
