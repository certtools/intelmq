# -*- coding: utf-8 -*-
"""
See docs/Feeds.md
"""

import sys

from datetime import datetime
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import FQDN, IPAddress, URL, DateTime
from intelmq.lib.message import Event


class Netlab360MagnitudeParserBot(ParserBot):

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
        else:
            lvalue = line.split('\t')
            event = Event(report)

            event.add('classification.identifier', lvalue[0].lower())
            event.add('time.source', DateTime.from_timestamp(int(lvalue[1])))
            if IPAddress.is_valid(lvalue[2]):
                event.add('source.ip', lvalue[2])

            if FQDN.is_valid(lvalue[3]):
                event.add('source.fqdn', lvalue[3])

            if URL.is_valid(lvalue[4]):
                event.add('source.url', lvalue[4])

            event.add('raw', line)
            event.add('classification.type', 'exploit')
            event.add('event_description.url', 'http://data.netlab.360.com/ek')

            yield event

if __name__ == "__main__":
    bot = Netlab360MagnitudeParserBot(sys.argv[1])
    bot.start()
