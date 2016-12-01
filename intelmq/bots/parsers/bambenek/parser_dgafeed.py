# -*- coding: utf-8 -*-
"""
See docs/Feeds.md
"""

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class BambenekDGAfeedParserBot(ParserBot):

    def parse_line(self, line, report):
        if line.startswith("#"):
            self.tempdata.append(line)
        else:
            lvalue = line.split(',')
            event = Event(report)

            event.add('source.fqdn', lvalue[0])
            event.add('event_description.text', lvalue[1])
            event.add('time.source', lvalue[2] + " 00:00 UTC")
            event.add('event_description.url', lvalue[3])
            event.add('classification.type', 'dga domain')
            event.add('raw', line)

            yield event

BOT = BambenekDGAfeedParserBot
