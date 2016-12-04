# -*- coding: utf-8 -*-
""" IntelMQ parser for Malc0de feeds """

import sys
import dateutil.parser

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class Malc0deParserBot(ParserBot):

    WINDOWS_FORMAT = {'http://malc0de.com/bl/BOOT',
                      'http://malc0de.com/bl/BOOT'}

    BIND_FORMAT = {'http://malc0de.com/bl/ZONES',
                   'https://malc0de.com/bl/ZONES'}

    IP_BLACKLIST = {'http://malc0de.com/bl/IP_Blacklist.txt',
                    'https://malc0de.com/bl/IP_Blacklist.txt'}

    def parse_line(self, line, report):
        lastgenerated = None

        if line.startswith('//') or len(line) == 0:
            self.tempdata.append(line)
            if '// Last updated' in line:
                self.lastgenerated = line.strip('// Last updated ')
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated + 'T00:00:00+00:00').isoformat()

        else:
            event = Event(report)
            if report['feed.url'] in Malc0deParserBot.WINDOWS_FORMAT:
                value = line.split(' ')[1]
                if self.lastgenerated:
                    event.add('time.source', self.lastgenerated)
                event.add('source.fqdn', value)
                event.add('classification.type', 'malware')
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)
                event.add('raw', line)

            if report['feed.url'] in Malc0deParserBot.BIND_FORMAT:
                value = line.split(' ')[1].strip('"')
                if self.lastgenerated:
                    event.add('time.source', self.lastgenerated)
                event.add('source.fqdn', value)
                event.add('classification.type', 'malware')
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)
                event.add('raw', line)

            if report['feed.url'] in Malc0deParserBot.IP_BLACKLIST:
                value = line.strip()
                if self.lastgenerated:
                    event.add('time.source', self.lastgenerated)
                event.add('source.ip', value)
                event.add('classification.type', 'malware')
                event.add('event_description.url', 'http://malc0de.com/database/index.php?search=' + value)
                event.add('raw', line)

            yield event

if __name__ == '__main__':
    bot = Malc0deParserBot(sys.argv[1])
    bot.start()
