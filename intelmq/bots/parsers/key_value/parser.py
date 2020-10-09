# -*- coding: utf-8 -*-
"""Parse a string of key=value pairs.

SPDX-FileCopyrightText: 2020 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Tokens which do not contain the kv_separator string are ignored.

Values cannot contain newlines.

Parameters:

    pair_separator: string, default ' ', string separating key=value
                    pairs

    kv_separator: string, default '=', string separating key and value

    keys: array of strings to strings, names of keys -> names of
          fields to propagate

    strip_quotes: boolean, default true, remove opening and closing
                  double quotes. Note that quotes do not protect pair
                  separation, so e.g. key="long value" will still be
                  split into 'key: "long' and 'value"'.

    timestamp_key: string, optional, key containing event timestamp.
                   Numerical values are interpreted as UNIX seconds,
                   others are parsed by
                   dateutil.parser.parse(fuzzy=True). If parsing fails
                   no timestamp field will be added.

"""

from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import ConfigurationError
from intelmq.lib.harmonization import DateTime

from dateutil.parser import parse


class KeyValueParserBot(ParserBot):

    def init(self):
        self.pair_separator = getattr(self.parameters, 'pair_separator', ' ')
        self.kv_separator = getattr(self.parameters, 'kv_separator', '=')
        self.keys = getattr(self.parameters, 'keys', {})
        if not self.keys:
            raise ConfigurationError('Key extraction', 'No keys specified.')
        self.strip_quotes = getattr(self.parameters, "strip_quotes", True)

    def parse_line(self, row, report):
        event = self.new_event(report)
        for kv_pair in row.split(self.pair_separator):
            (key, _, value) = kv_pair.rpartition(self.kv_separator)
            if not key:
                continue
            if self.strip_quotes and value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            if self.keys.get(key) == 'time.source':
                try:
                    if value.isnumeric():
                        value = DateTime.from_timestamp(int(value))
                    else:
                        value = parse(value, fuzzy=True).isoformat() + " UTC"
                except ValueError:
                    value = None  # Will be ignored by event.add()
                    self.logger.warn("Could not parse key %r for 'time.source'."
                                     " Ignoring this key in line %r.", (value, row))
            if key in self.keys:
                event.add(self.keys[key], value, raise_failure=False)
        event.add("raw", self.recover_line(row))
        yield event


BOT = KeyValueParserBot
