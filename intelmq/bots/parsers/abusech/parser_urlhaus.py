# -*- coding: utf-8 -*-
"""
Parses abuse.ch URLhaus feed in CSV format.

Docs:
 - https://urlhaus.abuse.ch/feeds/

Fields:
 - Dateadded (UTC)
 - URL
 - URL_status (offline, online)
 - Threat
 - Host
 - IPaddress
 - ASnumber
 - Country
"""

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event
from dateutil.parser import parse


class URLhausParserBot(ParserBot):

    parse = ParserBot.parse_csv
    recover_line = ParserBot.recover_line_csv
    ignore_lines_starting = ['#']

    def parse_line(self, row, report):
        event = Event(report)

        event.add('time.source', parse(row[0] + 'Z', fuzzy=True).isoformat())
        event.add('source.url', row[1])
        event.add('extra', {'status': row[2]})
        event.add('classification.identifier', row[3])
        event.add('source.fqdn', row[4])
        event.add('source.ip', row[5])
        event.add('source.asn', row[6])
        event.add('source.geolocation.cc', row[7])

        event.add('classification.type', 'malware')
        event.add('raw', self.recover_line(row))

        yield event


BOT = URLhausParserBot