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

        fields = top_line.split(',')
        if len(fields) is not len(FEEDS[feed]['format']):
            self.logger.warning(
                f"Feed '{feed}' has not the expected length of fields: {len(fields)} != {len(FEEDS[feed]['format'])}")
            raise PipelineError("Abusech ip parser bad config")

        for line in utils.base64_decode(report.get("raw")).splitlines():
            line = line.strip()
            if not any([line.startswith(prefix) for prefix in self.ignore_lines_starting]):
                yield line

    def parse_line(self, line, report):
        if line.startswith('#'):
            self.tempdata.append(line)
            if 'Generated on' in line:
                row = line.strip('# ')[13:]
                self.lastgenerated = dateutil.parser.parse(row).isoformat()
        else:
            event = self.new_event(report)
            self.__process_feed_fields(event, line, report['feed.url'])
            yield event

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])

    def __process_feed_fields(self, event, line, feed):
        event.add('classification.taxonomy', 'malicious code')
        event.add('classification.type', 'c&c')
        event.add('raw', line)

        current_feed_format = FEEDS[feed]['format']
        data = line.split(',') if len(current_feed_format) > 1 else line

        if isinstance(data, list):
            # has multiple fields
            i = 0
            for field in current_feed_format:
                event.add(field, data[i])
                i += 1
        else:
            # has only one 'ip' field
            event.add('time.source', self.lastgenerated)
            event.add('source.ip', line)
            event.add('malware.name', FEEDS[feed]['malware'])


BOT = AbusechIPParserBot
