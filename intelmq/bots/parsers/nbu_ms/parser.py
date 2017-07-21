# -*- coding: utf-8 -*-
"""
format:
Význam jednotlivých polí je následující:

    interní ID záznamu (například pro kontrolu) - zahodime
    název feedu (nyní vždycky "botnetfeed") - nepotrebujeme
    zdrojová IP adresa (nyní jen IPv4 adresy) - source.ip
    identifikace hrozby - malware.name
    první záznam v naší DB (ISO 8601, UTC) - nyní není zasílán a pole je prázdné - IGNORE
    poslední exportovaný záznam (ISO 8601, UTC) - time.source
    GeoIP latitude zdrojové IP adresy - IGNORE
    GeoIP longitude zdrojové IP adresy - IGNORE
    NETNAME záznam WHOIS zdrojové IP adresy z RIPE - IGNORE
    DESCR záznam WHOIS zdrojové IP adresy z RIPE - IGNORE
    zdrojová IP adresa je Tor exit node v době záznamu ("False" nebo "True") - comment

EX: ['204414df06f32af08a4a30c0', 'botnetfeed', '94.112.251.10', 'Conficker', '', '2017-07-01T23:56:41.886000', '50.0833', '14.4667', 'CZ-MOSILANA', 'Nova Mosilana a.s. Brno', 'False']

"""
from intelmq.lib.bot import ParserBot
import dateutil.parser
import pytz


class NbuMsParserBot(ParserBot):

    parse = ParserBot.parse_csv
    recover_line = ParserBot.recover_line_csv

    def parse_line(self, line, report):
        event = self.new_event(report)
        event.add("source.ip", line[2])
        event.add('classification.type', 'malware')
        event.add('malware.name', line[3])
        event.add('time.source', pytz.utc.localize(dateutil.parser.parse(line[5])).isoformat())
        event.add('comment', "TOR exit node: " + line[10])

        yield event


BOT = NbuMsParserBot
