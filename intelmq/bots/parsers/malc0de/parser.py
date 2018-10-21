# -*- coding: utf-8 -*-
""" IntelMQ parser for Malc0de feeds """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class Malc0deParserBot(ParserBot):

    WINDOWS_FORMAT = {'http://malc0de.com/bl/BOOT',
                      'https://malc0de.com/bl/BOOT'}

    BIND_FORMAT = {'http://malc0de.com/bl/ZONES',
                   'https://malc0de.com/bl/ZONES'}

    IP_BLACKLIST = {'http://malc0de.com/bl/IP_Blacklist.txt',
                    'https://malc0de.com/bl/IP_Blacklist.txt'}
    lastgenerated = None

    def parse_line(self, line, report):

        if line.startswith('//') or len(line) == 0:
            self.tempdata.append(line)
            if '// Last updated' in line:
                self.lastgenerated = line.strip('// Last updated ')
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated + 'T00:00:00+00:00').isoformat()

        else:
            event = self.new_event(report)
            if self.lastgenerated:
                event.add('time.source', self.lastgenerated)
            event.add('classification.type', 'malware')
            event.add('raw', line)

            if report['feed.url'] in Malc0deParserBot.WINDOWS_FORMAT:
                value = line.split(' ')[1]
                event.add('source.fqdn', value)
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)

            elif report['feed.url'] in Malc0deParserBot.BIND_FORMAT:
                value = line.split(' ')[1].strip('"')
                event.add('source.fqdn', value)
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)

            elif report['feed.url'] in Malc0deParserBot.IP_BLACKLIST:
                value = line.strip()
                event.add('source.ip', value)
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)

            else:
                raise ValueError('Unknown data feed %s.' % report['feed.url'])

            yield event


BOT = Malc0deParserBot
