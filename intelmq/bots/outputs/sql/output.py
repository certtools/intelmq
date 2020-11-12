# -*- coding: utf-8 -*-
"""
SQL output bot.

See :ref:`bot sql` bot documentation for installation and configuration.

In case of errors, the bot tries to reconnect if the error is of operational
and thus temporary. We don't want to catch too much, like programming errors
(missing fields etc).
"""

from intelmq.lib.bot import SQLBot


class SQLOutputBot(SQLBot):

    def init(self):
        super().init()
        self.table = self.parameters.table
        self.jsondict_as_string = getattr(self.parameters, 'jsondict_as_string', True)

    def process(self):
        event = self.receive_message().to_dict(jsondict_as_string=self.jsondict_as_string)

        keys = '", "'.join(event.keys())
        values = list(event.values())
        fvalues = len(values) * '{0}, '.format(self.format_char)
        query = ('INSERT INTO {table} ("{keys}") VALUES ({values})'
                 ''.format(table=self.table, keys=keys, values=fvalues[:-2]))

        if self.execute(query, values, rollback=True):
            self.con.commit()
            self.acknowledge_message()


BOT = SQLOutputBot
