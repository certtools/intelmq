# SPDX-FileCopyrightText: 2016 robcza
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
from typing import Optional, Union, Iterable

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
DOCS = "https://intelmq.readthedocs.io/en/latest/guides/Bots.html#generic-csv-parser"


class GenericCsvParserBot(ParserBot):
    """Parse generic CSV data. Ignoring lines starting with character #. URLs without protocol can be prefixed with a default value."""
    column_regex_search: Optional[dict] = None
    columns: Union[str, Iterable] = None
    compose_fields: Optional[dict] = {}
    columns_required: Optional[dict] = None
    data_type: Optional[dict] = None
    default_url_protocol: str = 'http://'
    delimiter: str = ','
    filter_text = None
    filter_type = None
    time_format = None
    type: Optional[str] = None
    type_translation = {}
    skip_header: bool = False

    def init(self):
        # convert columns to an array
        if type(self.columns) is str:
            self.columns = [column.strip() for column in self.columns.split(",")]

        if self.type_translation and isinstance(self.type_translation, str):  # not-empty string
            self.type_translation = json.loads(self.type_translation)
        elif not self.type_translation:  # empty string
            self.type_translation = {}
        self.data_type = json.loads(self.data_type or '{}')

        # prevents empty strings:
        self.column_regex_search = self.column_regex_search or {}

        # handle empty strings, false etc.
        if not self.time_format:
            self.time_format = None
        if self.time_format not in TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(TIME_CONVERSIONS.keys()),
                                  docs=DOCS)
        if self.filter_type and self.filter_type not in ('blacklist', 'whitelist'):
            raise InvalidArgument('filter_type', got=self.filter_type,
                                  expected=("blacklist", "whitelist"),
                                  docs=DOCS)

        if self.columns_required is None:
            self.columns_required = [True for _ in self.columns]
        if len(self.columns) != len(self.columns_required):
            raise ValueError("Length of parameters 'columns' (%d) and 'columns_required' (%d) "
                             "needs to be equal." % (len(self.columns), len(self.columns_required)))

        self.compose = self.compose_fields or {}

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        raw_report = raw_report.translate({0: None})
        # ignore lines starting with #. # can have leading spaces/tabs
        raw_report = re.sub(r'(?m)^[ \t]*#.*\n?', '', raw_report)
        # ignore null bytes
        raw_report = re.sub(r'(?m)\0', '', raw_report)
        # ignore lines having mix of spaces and tabs only
        raw_report = re.sub(r'(?m)^[ \t]*\n?', '', raw_report)
        # skip header
        if self.skip_header:
            self.tempdata.append(raw_report[:raw_report.find('\n')])
            raw_report = raw_report[raw_report.find('\n') + 1:]
        for row in csv.reader(io.StringIO(raw_report),
                              delimiter=str(self.delimiter)):

            if self.filter_text and self.filter_type:
                text_in_row = self.filter_text in self.delimiter.join(row)
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

        for keygroup, value, required in zip(self.columns, row, self.columns_required):
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
                        type = None
                        value = None

                if key in ("__IGNORE__", ""):
                    break

                if key in self.data_type:
                    value = DATA_CONVERSIONS[self.data_type[key]](value)

                if key in ("time.source", "time.destination"):
                    value = TIME_CONVERSIONS[self.time_format](value)
                elif key.endswith('.url'):
                    if not value:
                        continue
                    if '://' not in value:
                        value = self.default_url_protocol + value
                elif key in ["classification.type"] and self.type_translation:
                    if value in self.type_translation:
                        value = self.type_translation[value]
                    elif self.type is None:
                        continue
                if event.add(key, value, raise_failure=False) is not False:
                    break
            else:
                # if the value sill remains unadded we need to inform if the key is needed
                if required:
                    raise InvalidValue(key, value)

        # Field composing
        for key, value in self.compose.items():
            event[key] = value.format(*row)

        if self.type is not None and "classification.type" not in event:
            event.add('classification.type', self.type)
        event.add("raw", self.recover_line(row))
        yield event

    recover_line = ParserBot.recover_line_csv


BOT = GenericCsvParserBot
