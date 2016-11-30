# -*- coding: utf-8 -*-
""" Parser for IntelMQ and Nothink honeypot dns attack feed """

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import FQDN
from intelmq.lib.message import Event


class NothinkDNSAttackParserBot(ParserBot):
    """ Nothink DNS Attack Bot """

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)

        else:
            line = line.strip('"').split('","')
            event = Event(report)
            event.add('time.source', line[0] + '+00:00')
            event.add('source.ip', line[1])
            event.add('source.asn', line[2])
            event.add('source.as_name', line[3])
            if line[4] not in ['.', 'n/a', 'bka']:
                event.add('source.reverse_dns', line[4])
            if line[5] != 'UNK':
                event.add('source.geolocation.cc', line[5])
            event.add('classification.type', 'ddos')
            event.add('event_description.text', 'On time.source the source.ip was seen'
                                                ' performing DNS amplification attacks against honeypots')
            event.add('protocol.application', 'dns')
            event.add('raw', ','.join(line))

            yield event

if __name__ == '__main__':
    bot = NothinkDNSAttackParserBot(sys.argv[1])
    bot.start()
