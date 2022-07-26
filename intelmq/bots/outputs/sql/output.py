# SPDX-FileCopyrightText: 2019 Edvard Rejthar
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
        values = itemgetter_tuple(*valid_keys)(event)
        fvalues = len(values) * '{0}, '.format(self.format_char)
        query = ('INSERT INTO {table} ("{keys}") VALUES ({values})'
                 ''.format(table=self.table, keys=keys, values=fvalues[:-2]))

        if self.execute(query, values, rollback=True):
            self.con.commit()
            self.acknowledge_message()


BOT = SQLOutputBot
