# SPDX-FileCopyrightText: 2019 Brajneesh Kumar
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
HTML Table parser

Parameters:
columns: string
ignore_values: string
skip_table_head: boolean
attribute_name: string
attribute_value: string
table_index: int
split_column: string
split_separator: string
split_index: int
default_url_protocol: string
time_format: string
type: string
"""

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import DateTime
from intelmq.lib.exceptions import MissingDependencyError


try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    bs = None


class HTMLTableParserBot(Bot):
    """Parse HTML table data"""
    attribute_name = ""
    attribute_value = ""
    columns = ["", "source.fqdn"]
    default_url_protocol = 'http://'
    ignore_values = None
    skip_table_head = True
    split_column = ""
    split_index = 0
    split_separator = None
    table_index = 0
    time_format = None
    type = "c2-server"
    _parser = 'html.parser'

    def init(self):
        if bs is None:
            raise MissingDependencyError("beautifulsoup4")

        # convert columns to an array
        if type(self.columns) is str:
            self.columns = [column.strip() for column in self.columns.split(",")]
        if self.ignore_values is None:
            self.ignore_values = len(self.columns) * ['']
        if type(self.ignore_values) is str:
            self.ignore_values = [value.strip() for value in self.ignore_values.split(",")]

        if len(self.columns) != len(self.ignore_values):
            raise ValueError("Length of parameters 'columns' and 'ignore_values' is not equal.")

        self.attr_name = self.attribute_name
        self.attr_value = self.attribute_value
        self.skip_head = self.skip_table_head
        self.skip_row = 1 if self.skip_head else 0

        if self.time_format and self.time_format.split('|')[0] not in DateTime.TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(DateTime.TIME_CONVERSIONS.keys()),
                                  docs='https://intelmq.readthedocs.io/en/latest/guides/Bots.html#html-table-parser')

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, self._parser)
        if self.attr_name:
            table = soup.find_all('table', attrs={self.attr_name: self.attr_value})
            self.logger.debug('Found %d table(s) by attribute %r: %r.',
                              len(table), self.attr_name, self.attr_value)
        else:
            table = soup.find_all('table')
            self.logger.debug('Found %d table(s).', len(table))
        table = table[self.table_index]

        rows = table.find_all('tr')[self.skip_row:]
        self.logger.debug('Handling %d row(s).', len(rows))

        for feed in rows:

            event = self.new_event(report)
            tdata = [data.text for data in feed.find_all('td')]

            data_added = False
            for key, data, ignore_value in zip(self.columns, tdata, self.ignore_values):
                keys = key.split('|') if '|' in key else [key, ]
                data = data.strip()
                if data == ignore_value:
                    continue
                for key in keys:
                    if isinstance(data, str) and not data:  # empty string is never valid
                        break

                    if key in ["__IGNORE__", ""]:
                        break

                    if self.split_column and key == self.split_column:
                        data = data.split(self.split_separator)[int(self.split_index)]
                        data = data.strip()

                    if key in ["time.source", "time.destination"]:
                        try:
                            data = int(data)
                        except ValueError:
                            pass
                        data = DateTime.convert(data, format=self.time_format)

                    elif key.endswith('.url'):
                        if not data:
                            continue
                        if '://' not in data:
                            data = self.default_url_protocol + data

                    if event.add(key, data, raise_failure=False):
                        data_added = True
                        break
                else:
                    raise ValueError("Could not add value %r to %s, all invalid."
                                     "" % (data, keys))

            if not data_added:
                # we added nothing from this row, so skip it
                continue
            if self.type is not None and "classification.type" not in event:
                event.add('classification.type', self.type)
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = HTMLTableParserBot
