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


class GenericCsvParserBot(ParserBot):

    def init(self):
        self.type_translation = None

        self.columns = self.parameters.columns
        # convert columns to an array
        if type(self.columns) is str:
            self.columns = [column.strip() for column in self.columns.split(",")]

        if hasattr(self.parameters, 'type_translation'):
            self.type_translation = json.loads(self.parameters.type_translation)

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        # ignore lines starting with #
        raw_report = re.sub(r'(?m)^#.*\n?', '', raw_report)
        # ignore null bytes
        raw_report = re.sub(r'(?m)\0', '', raw_report)
        # skip header
        if hasattr(self.parameters, 'skip_header') and self.parameters.skip_header:
            raw_report = raw_report[raw_report.find('\n') + 1:]
        for row in csv.reader(io.StringIO(raw_report),
                              delimiter=str(self.parameters.delimiter)):
            yield row

    def parse_line(self, row, report):
        event = self.new_event(report)

        for key, value in zip(self.columns, row):

            if key in ["__IGNORE__", ""]:
                continue
            if key in ["time.source", "time.destination"]:
                value = parse(value, fuzzy=True).isoformat()
                value += " UTC"
            elif key.endswith('.url') and '://' not in value:
                value = self.parameters.default_url_protocol + value
            elif key in ["classification.type"] and self.type_translation:
                if value in self.type_translation:
                    value = self.type_translation[value]
                elif not hasattr(self.parameters, 'type'):
                    continue
            event.add(key, value)

        if hasattr(self.parameters, 'type')\
                and "classification.type" not in event:
            event.add('classification.type', self.parameters.type)
        event.add("raw", self.recover_line(row))
        yield event

    recover_line = ParserBot.recover_line_csv


BOT = GenericCsvParserBot
