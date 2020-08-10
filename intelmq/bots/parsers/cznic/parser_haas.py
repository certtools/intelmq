# -*- coding: utf-8 -*-
import dateutil.parser

from intelmq.lib.bot import ParserBot


class CZNICHaasParserBot(ParserBot):

    parse = ParserBot.parse_json
    recover_line = ParserBot.recover_line_json

    def parse_line(self, line, report):
        event = self.new_event(report)

        event.add('source.ip', line['ip'])
        event.add('time.source', str(dateutil.parser.parse(line["time"])))
        event.add('protocol.transport', 'tcp')
        event.add('protocol.application', 'ssh')
        event.add('destination.port', 22)
        event.add('extra', {k: v for k, v in line.items() if k in {"time_closed", "commands"}})
        event.add('raw', self.recover_line(line))

        if line["country"]:
            event.add("source.geolocation.cc", line["country"])

        if line["login_successful"] and line["commands"]:
            event.add('classification.type', 'unauthorized-command')

        elif line["login_successful"] and not line["commands"]:
            event.add('classification.type', 'unauthorized-login')

        else:
            event.add('classification.type', 'brute-force')
            event.add('extra.count', 1)

        yield event


BOT = CZNICHaasParserBot
