# -*- coding: utf-8 -*-
"""
PostgreSQL output bot.

See Readme.md for installation and configuration.

In case of errors, the bot tries to reconnect if the error is of operational
and thus temporary. We don't want to catch too much, like programming errors
(missing fields etc).
"""
from __future__ import unicode_literals
import sys

import psycopg2
from intelmq.lib.bot import Bot


class PostgreSQLBot(Bot):

    def init(self):
        self.logger.debug("Connecting to PostgreSQL")
        try:
            if hasattr(self.parameters, 'connect_timeout'):
                connect_timeout = self.parameters.connect_timeout
            else:
                connect_timeout = 5

            self.con = psycopg2.connect(database=self.parameters.database,
                                        user=self.parameters.user,
                                        password=self.parameters.password,
                                        host=self.parameters.host,
                                        port=self.parameters.port,
                                        sslmode=self.parameters.sslmode,
                                        connect_timeout=connect_timeout,
                                        )
            self.cur = self.con.cursor()
            self.con.autocommit = getattr(self.parameters, 'autocommit', True)

            self.table = self.parameters.table
        except:
            self.logger.exception('Failed to connect to database')
            self.stop()
        self.logger.info("Connected to PostgreSQL")

    def process(self):
        event = self.receive_message()

        if not event:
            self.acknowledge_message()
            return

        keys = '", "'.join(event.keys())
        values = event.values()
        fvalues = len(values) * '%s, '
        query = ('INSERT INTO {table} ("{keys}") VALUES ({values})'
                 ''.format(table=self.table, keys=keys, values=fvalues[:-2]))

        self.logger.debug('Query: {!r} with values {!r}'.format(query, values))
        try:
            # note: this assumes, the DB was created with UTF-8 support!
            self.cur.execute(query, values)
        except (psycopg2.InterfaceError, psycopg2.InternalError,
                psycopg2.OperationalError, AttributeError):
            try:
                self.con.rollback()
                self.logger.exception('Executed rollback command '
                                      'after failed query execution.')
            except Exception:
                self.logger.exception('Cursor has been closed, connecting '
                                      'again.')
                self.init()
        else:
            self.con.commit()
            self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot(sys.argv[1])
    bot.start()
