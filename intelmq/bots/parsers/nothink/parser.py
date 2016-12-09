# -*- coding: utf-8 -*-

import dateutil

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event

SOURCE_FEEDS = {'http://www.nothink.org/blacklist/blacklist_snmp_day.txt': 'snmp',
                'http://www.nothink.org/blacklist/blacklist_ssh_day.txt': 'ssh',
                'http://www.nothink.org/blacklist/blacklist_telnet_day.txt': 'telnet'}


class NothinkParserBot(ParserBot):
    lastgenerated = None

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
            if 'Generated' in line:
                row = line.strip('# ')[10:]
                self.lastgenerated = dateutil.parser.parse(row).isoformat()
        else:
            event = Event(report)
            event.add('time.source', self.lastgenerated + ' UTC')
            event.add('source.ip', line)
            event.add('classification.type', 'scanner')
            event.add('protocol.application', SOURCE_FEEDS[report['feed.url']])
            event.add('raw', line)

            yield event

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])

BOT = NothinkParserBot
