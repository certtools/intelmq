# -*- coding: utf-8 -*-
from intelmq.lib.bot import ParserBot
import dateutil.parser
import pytz


class HaasParserBot(ParserBot):

    parse = ParserBot.parse_json
    recover_line = ParserBot.recover_line_json

    def parse_line(self, line, report):
        event = self.new_event(report)
        event.add('classification.type', 'unauthorized-command')
        event.add("source.ip", line["ip"])
        event.add("source.geolocation.cc", line["country"])
        event.add('time.source', str(dateutil.parser.parse(line["time"])))
        event.add('extra.haas', {k: v for k, v in line.items() if k in {"time_closed", "commands"}})

        yield event


BOT = HaasParserBot
