# -*- coding: utf-8 -*-
"""
Parses simple newline separated list of IPs.

Docs:
 - https://feodotracker.abuse.ch/blocklist/
 - https://zeustracker.abuse.ch/blocklist.php
"""
import re

import dateutil

from intelmq.lib.bot import ParserBot
from intelmq.lib import utils
from intelmq.lib.exceptions import PipelineError

FEEDS = {
    'https://feodotracker.abuse.ch/downloads/ipblocklist.csv': {
        'format': [
            'time.source',
            'source.ip',
            'source.port',
            'malware.name'
        ],
        'malware': 'Cridex'
    },
    'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist': {
        'format': [
            'source.ip'
        ],
        'malware': 'Zeus'
    },
    'https://zeustracker.abuse.ch/blocklist.php?download=badips': {
        'format': [
            'source.ip'
        ],
        'malware': 'Zeus'
    }
}


class AbusechIPParserBot(ParserBot):
    lastgenerated = None

    def parse(self, report: dict):
        lines = utils.base64_decode(report.get("raw")).splitlines()
        regex = re.compile(r'^#+.*')  # filter out comments
        top_line = list(filter(lambda i: not regex.search(i), lines))[0]
        feed = report['feed.url']
        # TODO: Edit lastgenerated to correspond to the date in the feed file header online

        fields = top_line.split(',')
        if len(fields) is not len(FEEDS[feed]['format']):
            self.logger.warning(
                f"Feed '{feed}' has not the expected length of fields: {len(fields)} != {len(FEEDS[feed]['format'])}")
            raise PipelineError("Abusech ip parser is not up to date with the format online")

        for line in utils.base64_decode(report.get("raw")).splitlines():
            line = line.strip()
            if not any([line.startswith(prefix) for prefix in self.ignore_lines_starting]):
                yield line

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
            if 'Last updated' in line:
                self.lastgenerated = dateutil.parser.parse(
                    re.search('[0-9]{4}.[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}( UTC)?', line).group(0)).isoformat()
        else:
            event = self.new_event(report)
            self.__process_defaults(event, line, report['feed.url'])
            self.__process_fields(event, line, report['feed.url'])
            print(f'------------------ event: {event}')
            yield event

    def __process_defaults(self, event, line, feed_url):
        defaults = set([
            ('time.source', None),
            ('malware.name', FEEDS[feed_url]['malware']),
            ('raw', line),
            ('classification.type', 'c&c'),
            ('classification.taxonomy', 'malicious code'),
            ('time.observation', self.lastgenerated)
        ])

        for i in defaults:
            if i[0] not in FEEDS[feed_url]['format']:
                if i[0] == 'time.observation' and i[1] is not None:
                    print(f'------------------ is: {i[0]} {i[1]}')
                    event.add(i[0], i[1], overwrite=True)
                elif i[0] != 'time.observation':
                    event.add(i[0], i[1])
                else:
                    pass

    def __process_fields(self, event, line, feed_url):
        for field, value in zip(FEEDS[feed_url]['format'], line.split(',')):
            event.add(field, value)

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])


BOT = AbusechIPParserBot
