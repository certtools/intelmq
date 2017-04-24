# -*- coding: utf-8 -*-
"""
Generic CSV parser

Parameters:
columns: string
delimiter: string
default_url_protocol: string
skip_header: boolean
type: string
type_translation: string

"""
import csv
import io
import json
import re

from dateutil.parser import parse

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import DateTime


TIME_CONVERSIONS = {'timestamp': DateTime.from_timestamp,
                    'windows_nt': DateTime.from_windows_nt,
                    None: lambda value: parse(value, fuzzy=True).isoformat() + " UTC"}


class GenericCsvParserBot(ParserBot):

    def init(self):
        self.columns = self.parameters.columns
        # convert columns to an array
        if type(self.columns) is str:
            self.columns = [column.strip() for column in self.columns.split(",")]

        self.type_translation = json.loads(getattr(self.parameters, 'type_translation', None) or '{}')

        # prevents empty strings:
        self.column_regex_search = getattr(self.parameters, 'column_regex_search', None) or {}

        self.time_format = getattr(self.parameters, "time_format", None)
        if self.time_format not in TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(TIME_CONVERSIONS.keys()),
                                  docs='docs/Bots.md')

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        # ignore lines starting with #
        raw_report = re.sub(r'(?m)^#.*\n?', '', raw_report)
        # ignore null bytes
        raw_report = re.sub(r'(?m)\0', '', raw_report)
        # skip header
        if getattr(self.parameters, 'skip_header', False):
            raw_report = raw_report[raw_report.find('\n') + 1:]
        for row in csv.reader(io.StringIO(raw_report),
                              delimiter=str(self.parameters.delimiter)):
            yield row

    def parse_line(self, row, report):
        event = self.new_event(report)

        extra = {}
        for key, value in zip(self.columns, row):
            regex = self.column_regex_search.get(key, None)
            if regex:
                search = re.search(regex, value)
                if search:
                    value = search.group(0)
                else:
                    value = None

            if key in ["__IGNORE__", ""]:
                continue
            if key in ["time.source", "time.destination"]:
                value = TIME_CONVERSIONS[self.time_format](value)
            elif key.endswith('.url') and '://' not in value:
                value = self.parameters.default_url_protocol + value
            elif key in ["classification.type"] and self.type_translation:
                if value in self.type_translation:
                    value = self.type_translation[value]
                elif not hasattr(self.parameters, 'type'):
                    continue
            if key.startswith('extra.'):
                if value:
                    extra[key[6:]] = value
            else:
                event.add(key, value)

        if hasattr(self.parameters, 'type')\
                and "classification.type" not in event:
            event.add('classification.type', self.parameters.type)
        event.add("raw", self.recover_line(row))
        if extra:
            event.add('extra', extra)
        yield event

    recover_line = ParserBot.recover_line_csv


BOT = GenericCsvParserBot
