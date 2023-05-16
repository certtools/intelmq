# SPDX-FileCopyrightText: 2019 Edvard Rejthar, 2022 Intevation GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
SQL output bot.

See :ref:`bot sql` bot documentation for installation and configuration.

In case of errors, the bot tries to reconnect if the error is of operational
and thus temporary. We don't want to catch too much, like programming errors
(missing fields etc).
"""

from intelmq.lib.bot import OutputBot
from intelmq.lib.mixins import SQLMixin


def itemgetter_tuple(*items):
    def g(obj):
        return tuple(obj[item] for item in items)
    return g


class SQLOutputBot(OutputBot, SQLMixin):
    """Send events to a PostgreSQL or SQLite database"""
    autocommit = True
    database = "intelmq-events"
    engine = None
    host = "localhost"
    jsondict_as_string = True
    password = None
    port = "5432"
    sslmode = "require"
    table = 'events'
    user = "intelmq"
    fields = None

    def init(self):
        super().init()

    def process(self):
        event = self.receive_message().to_dict(jsondict_as_string=self.jsondict_as_string)

        key_names = self.fields
        if key_names is None:
            key_names = event.keys()
        valid_keys = [key for key in key_names if key in event]
        keys = '", "'.join(valid_keys)
        values = self.prepare_values(itemgetter_tuple(*valid_keys)(event))
        fvalues = len(values) * f'{self.format_char}, '
        query = ('INSERT INTO {table} ("{keys}") VALUES ({values})'
                 ''.format(table=self.table, keys=keys, values=fvalues[:-2]))

        if self.execute(query, values, rollback=not self.fail_on_errors):
            self.con.commit()
            self.acknowledge_message()

    def prepare_values(self, values):
        if self._engine_name == self.POSTGRESQL:
            # escape JSON-encoded NULL characters. JSON escapes them once, but we need to escape them twice,
            # so that Postgres does not encounter a NULL char while decoding it
            # https://github.com/certtools/intelmq/issues/2203
            return [value.replace('\\u0000', '\\\\u0000') if isinstance(value, str) else value for value in values]
        else:
            return list(values)


BOT = SQLOutputBot
