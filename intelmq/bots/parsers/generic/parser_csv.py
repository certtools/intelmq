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
data_type: string

"""
import csv
import io
import json
import re

from dateutil.parser import parse

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidArgument, InvalidValue
from intelmq.lib.harmonization import DateTime


TIME_CONVERSIONS = {'timestamp': DateTime.from_timestamp,
                    'windows_nt': DateTime.from_windows_nt,
                    'epoch_millis': DateTime.from_epoch_millis,
                    None: lambda value: parse(value, fuzzy=True).isoformat() + " UTC"}

DATA_CONVERSIONS = {'json': lambda data: json.loads(data)}


class GenericCsvParserBot(ParserBot):

    def init(self):
        self.columns = self.parameters.columns
        # convert columns to an array
        if type(self.columns) is str:
            self.columns = [column.strip() for column in self.columns.split(",")]

        self.type_translation = json.loads(getattr(self.parameters, 'type_translation', None) or '{}')
        self.data_type = json.loads(getattr(self.parameters, 'data_type', None) or '{}')

        # prevents empty strings:
        self.column_regex_search = getattr(self.parameters, 'column_regex_search', None) or {}

        self.time_format = getattr(self.parameters, "time_format", None)
        if self.time_format not in TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(TIME_CONVERSIONS.keys()),
                                  docs='docs/Bots.md')
        self.filter_text = getattr(self.parameters, 'filter_text', None)
        self.filter_type = getattr(self.parameters, 'filter_type', None)
        if self.filter_type and self.filter_type not in ('blacklist', 'whitelist'):
            raise InvalidArgument('filter_type', got=self.filter_type,
                                  expected=("blacklist", "whitelist"),
                                  docs='docs/Bots.md')

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        raw_report = raw_report.translate({0: None})
        # ignore lines starting with #
        raw_report = re.sub(r'(?m)^#.*\n?', '', raw_report)
        # ignore null bytes
        raw_report = re.sub(r'(?m)\0', '', raw_report)
        # skip header
        if getattr(self.parameters, 'skip_header', False):
            self.tempdata.append(raw_report[:raw_report.find('\n')])
            raw_report = raw_report[raw_report.find('\n') + 1:]
        for row in csv.reader(io.StringIO(raw_report),
                              delimiter=str(self.parameters.delimiter)):

            if self.filter_text and self.filter_type:
                text_in_row = self.filter_text in self.parameters.delimiter.join(row)
                if text_in_row and self.filter_type == 'whitelist':
                    yield row
                elif not text_in_row and self.filter_type == 'blacklist':
                    yield row
                else:
                    continue
            else:
                yield row

    def parse_line(self, row, report):
        event = self.new_event(report)

        for keygroup, value in zip(self.columns, row):
            keys = keygroup.split('|') if '|' in keygroup else [keygroup, ]
            for key in keys:
                if isinstance(value, str) and not value:  # empty string is never valid
                    break
                regex = self.column_regex_search.get(key, None)
                if regex:
                    search = re.search(regex, value)
                    if search:
                        value = search.group(0)
                    else:
                        value = None

                if key in ["__IGNORE__", ""]:
                    break

                if key in self.data_type:
                    value = DATA_CONVERSIONS[self.data_type[key]](value)

                if key in ["time.source", "time.destination"]:
                    value = TIME_CONVERSIONS[self.time_format](value)
                elif key.endswith('.url'):
                    if not value:
                        continue
                    if '://' not in value:
                        value = self.parameters.default_url_protocol + value
                elif key in ["classification.type"] and self.type_translation:
                    if value in self.type_translation:
                        value = self.type_translation[value]
                    elif not hasattr(self.parameters, 'type'):
                        continue
                if event.add(key, value, raise_failure=False):
                    break
            else:
                # if the value sill remains unadded we need to inform
                raise InvalidValue(key, value)

        if hasattr(self.parameters, 'type')\
                and "classification.type" not in event:
            event.add('classification.type', self.parameters.type)
        event.add("raw", self.recover_line(row))
        yield event

    recover_line = ParserBot.recover_line_csv


BOT = GenericCsvParserBot
