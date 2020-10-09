# -*- coding: utf-8 -*-
"""
Parses simple newline separated list of IPs.

Docs:
 - https://feodotracker.abuse.ch/blocklist/
 - https://zeustracker.abuse.ch/blocklist.php
"""
import re

import dateutil

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime

FEEDS = {
    'https://feodotracker.abuse.ch/downloads/ipblocklist.csv': {
        'format': [
            'extra.first_seen',
            'source.ip',
            'source.port',
            'extra.last_online',
            'malware.name'
        ],
        'malware': 'feodo',
        'position': 2,
        'additional_fields':
            {
                'time.source': lambda row: row[3] + 'T00:00+00' if row[3] else row[0] + ' UTC',
        },
    },
    'https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist': {
        'format': [
            'source.ip'
        ],
        'malware': 'zeus',
        'position': 1
    },
    'https://zeustracker.abuse.ch/blocklist.php?download=badips': {
        'format': [
            'source.ip'
        ],
        'malware': 'zeus',
        'position': 1
    }
}


class AbusechIPParserBot(ParserBot):
    __last_generated_date = None
    __is_comment_line_regex = re.compile(r'^#+.*')
    __date_regex = re.compile(r'[0-9]{4}.[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}( UTC)?')

    def parse(self, report: dict):
        feed = report['feed.url']

        raw_lines = utils.base64_decode(report.get("raw")).splitlines()
        self.comments = list(r for r in raw_lines if self.__is_comment_line_regex.search(r))

        fields = self.comments[-FEEDS[feed]['position']].split(',')
        if len(fields) is not len(FEEDS[feed]['format']):
            self.logger.warning("Feed '{}' has not the expected fields: {} != {}".format(feed,
                                                                                         len(fields),
                                                                                         len(FEEDS[feed]['format'])))
            raise ValueError("Abusech ip parser is not up to date with the format online")

        for line in self.comments:
            if 'Last updated' in line:
                self.__last_generated_date = dateutil.parser.parse(self.__date_regex.search(line).group(0)).isoformat()

        lines = (line for line in raw_lines if not self.__is_comment_line_regex.search(line))
        for line in lines:
            yield line.strip()

    def parse_line(self, line, report):
        event = self.new_event(report)
        self.__process_defaults(event, line, report['feed.url'])
        self.__process_fields(event, line, report['feed.url'])
        self.__process_additional(event, line, report['feed.url'])
        yield event

    def __process_defaults(self, event, line, feed_url):
        defaults = {
            ('malware.name', FEEDS[feed_url]['malware']),
            ('raw', self.recover_line(line)),
            ('classification.type', 'c2server'),
            ('classification.taxonomy', 'malicious code'),
            ('extra.feed_last_generated', self.__last_generated_date)
        }

        for i in defaults:
            if i[0] not in FEEDS[feed_url]['format']:
                if i[1] is None:
                    continue
                else:
                    event.add(i[0], i[1], overwrite=True)

    @staticmethod
    def __process_fields(event, line, feed_url):
        for field, value in zip(FEEDS[feed_url]['format'], line.split(',')):
            if value and field in ('extra.first_seen', 'extra.last_online'):
                if ':' in value:
                    event.add(field, DateTime.sanitize(value + '+00:00'))
                else:
                    event.add(field, value + 'T00:00:00+00:00')
            else:
                event.add(field, value)

    @staticmethod
    def __process_additional(event, line, feed_url):
        if 'additional_fields' not in FEEDS[feed_url]:
            return
        for field, function in FEEDS[feed_url]['additional_fields'].items():
            event.add(field, function(line.split(',')))

    def recover_line(self, line):
        return '\n'.join(self.comments + [line])


BOT = AbusechIPParserBot
