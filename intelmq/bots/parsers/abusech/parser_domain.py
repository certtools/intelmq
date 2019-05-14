# -*- coding: utf-8 -*-
"""
Parses simple newline separated list of domains.

Docs:
 - https://feodotracker.abuse.ch/blocklist/
 - https://palevotracker.abuse.ch/blocklists.php
 - https://zeustracker.abuse.ch/blocklist.php
"""


import dateutil.parser

from intelmq.lib.bot import ParserBot

SOURCE_FEEDS = {'https://feodotracker.abuse.ch/blocklist/?download=domainblocklist': 'Cridex',
                'https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist': 'Palevo',
                'https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist': 'Zeus',
                'https://zeustracker.abuse.ch/blocklist.php?download=baddomains': 'Zeus'}


class AbusechDomainParserBot(ParserBot):
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
            event.add('classification.taxonomy', 'malicious code')
            event.add('classification.type', 'c2server')
            event.add('source.fqdn', line)
            event.add("raw", line)
            event.add("malware.name", SOURCE_FEEDS[report["feed.url"]])
            yield event

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])


BOT = AbusechDomainParserBot
