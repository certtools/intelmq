# -*- coding: utf-8 -*-

from intelmq.lib.bot import ParserBot


class DragonResearchGroupSSHParserBot(ParserBot):

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
        else:
            splitted_row = line.split('|')
            event = self.new_event(report)

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
            event.add("protocol.application", "ssh")
            event.add("protocol.transport", "tcp")
            event.add("destination.port", 22)
            event.add("raw", line)

            yield event


BOT = DragonResearchGroupSSHParserBot
