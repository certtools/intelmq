# -*- coding: utf-8 -*-
import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class DragonResearchGroupVNCParserBot(ParserBot):

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
        else:
            splitted_row = line.split('|')
            event = Event(report)

            columns = ["source.asn", "source.as_name",
                       "source.ip", "time.source"]

            for key, value in zip(columns, splitted_row):
                value = value.strip()

                if key == "time.source":
                    value += "+00:00"

                if value == "NA":
                    continue

                event.add(key, value)

            event.add("classification.type", "brute-force")
            event.add("protocol.application", "vnc")
            event.add("protocol.transport", "tcp")
            event.add("raw", line)

            yield event


if __name__ == "__main__":
    bot = DragonResearchGroupVNCParserBot(sys.argv[1])
    bot.start()
