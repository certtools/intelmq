# -*- coding: utf-8 -*-
""" Parser for Bitcash blocklist feed. """

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class BitcashBlocklistParserBot(ParserBot):
    """ Parser for Bitcash blocklist feed. """

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)

        else:
            line = line.split()
            event = Event(report)
            event.add('time.source', line[5] + 'T' + line[6] + '+00:00')
            event.add('source.ip', line[0])
            event.add('source.reverse_dns', line[2], raise_failure=False)
            event.add('classification.type', 'scanner')
            event.add('event_description.text', 'IPs banned for serious abusing of Bitcash services '
                                                '(scanning, sniffing, harvesting, dos attacks)')
            event.add('raw', ','.join(line))

            yield event

BOT = BitcashBlocklistParserBot
