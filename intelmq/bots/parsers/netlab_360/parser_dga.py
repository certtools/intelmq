# -*- coding: utf-8 -*-
"""
See docs/Feeds.md
"""

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import FQDN
from intelmq.lib.message import Event


class Netlab360DGAParserBot(ParserBot):

    def parse_line(self, line, report):
        if line.startswith('#') or len(line) == 0:
            self.tempdata.append(line)
        else:
            lvalue = line.split('\t')
            event = Event(report)

            event.add('classification.identifier', lvalue[0].lower())
            event.add('source.fqdn', lvalue[1])
            event.add('time.source', lvalue[3] + " UTC")
            event.add('raw', line)
            event.add('classification.type', 'c&c')
            event.add('event_description.url', 'http://data.netlab.360.com/dga')

            yield event

if __name__ == "__main__":
    bot = Netlab360DGAParserBot(sys.argv[1])
    bot.start()
