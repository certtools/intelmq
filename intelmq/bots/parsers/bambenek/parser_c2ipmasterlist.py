# -*- coding: utf-8 -*-
"""
Se docs/Feeds.md
"""

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class Bambenekc2ipmasterlistParserBot(ParserBot):

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
        else:
            lvalue = line.split(',')
            event = Event(report)

            event.add('source.ip', lvalue[0])
            event.add('event_description.text', lvalue[1])
            event.add('time.source', lvalue[2] + " UTC")
            event.add('event_description.url', lvalue[3])
            event.add('classification.type', 'c&c')
            event.add('status', 'online')
            event.add('raw', line)

            yield event

if __name__ == "__main__":
    bot = Bambenekc2ipmasterlistParserBot(sys.argv[1])
    bot.start()
