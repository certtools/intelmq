# -*- coding: utf-8 -*-
"""
Completely untested. If you have example data, please contact us!
"""

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class ArborParserBot(ParserBot):

    def parse_line(self, row, report):
        if row.startswith('other'):
            return

        event = Event(report)

        event.add('classification.type', 'brute-force')
        event.add("raw", row)

        columns = ["source.ip"]
        row = row.split()

        for key, value in zip(columns, row):
            event.add(key, value)

        yield event


if __name__ == "__main__":
    bot = ArborParserBot(sys.argv[1])
    bot.start()
