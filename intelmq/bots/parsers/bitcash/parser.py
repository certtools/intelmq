# -*- coding: utf-8 -*-
""" Parser for Bitcash blocklist feed. """

import sys

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import FQDN
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
            if FQDN.is_valid(line[2]):
                event.add('source.reverse_dns', line[2])
            event.add('classification.type', 'scanner')
            event.add('event_description.txt', 'IPs banned for serious abusing of Bitcash services \
                                               (scanning, sniffing, harvesting, dos attacks)')
            event.add('raw', line)

            yield event

if __name__ == '__main__':
    bot = BitcashBlocklistParserBot(sys.argv[1])
    bot.start()
