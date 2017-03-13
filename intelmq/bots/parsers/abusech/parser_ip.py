# -*- coding: utf-8 -*-
"""
Parsers simple newline separated list of IPs.

Docs:
 - https://feodotracker.abuse.ch/blocklist/
 - https://zeustracker.abuse.ch/blocklist.php
"""


import dateutil

from intelmq.lib.bot import ParserBot

SOURCE_FEEDS = {'https://feodotracker.abuse.ch/blocklist/?download=ipblocklist': 'Cridex',
                'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist': 'Zeus',
                'https://zeustracker.abuse.ch/blocklist.php?download=badips': 'Zeus'}


class AbusechIPParserBot(ParserBot):
    lastgenerated = None

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
            if 'Generated on' in line:
                row = line.strip('# ')[13:]
                self.lastgenerated = dateutil.parser.parse(row).isoformat()
        else:
            event = self.new_event(report)
            event.add('time.source', self.lastgenerated)
            event.add('classification.type', 'c&c')
            event.add('source.ip', line)
            event.add("raw", line)
            event.add("malware.name", SOURCE_FEEDS[report["feed.url"]])
            yield event

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])


BOT = AbusechIPParserBot
