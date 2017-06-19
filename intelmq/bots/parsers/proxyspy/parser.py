# -*- coding: utf-8 -*-
""" IntelMQ Parser for Proxyspy """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class ProxyspyParserBot(ParserBot):
    lastgenerated = None

    def parse_line(self, line, report):
        if line.startswith('P') or line.startswith('I') or line.startswith('F') or len(line) == 0:
            self.tempdata.append(line)
            if 'Proxy list updated at' in line:
                self.lastgenerated = line.strip('Proxy list updated at')[5:]
                self.lastgenerated = dateutil.parser.parse(self.lastgenerated).isoformat()

        else:
            value = line.split(' ')
            event = self.new_event(report)
            event.add('time.source', self.lastgenerated)
            event.add('source.ip', value[0].split(':')[0])
            event.add('source.port', value[0].split(':')[1])
            event.add('source.geolocation.cc', value[1].split('-')[0])
            event.add('event_description.text', 'Possible HTTP/HTTPS proxy usage when IP and port match for '
                                                'outbound traffic.')
            event.add('classification.type', 'proxy')
            event.add('raw', line)

            yield event


BOT = ProxyspyParserBot
