# -*- coding: utf-8 -*-
"""
Generic DB Lookup
"""

from intelmq.lib.bot import Bot

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None


class GenericDBLookupExpertBot(Bot):

    def init(self):
        self.logger.debug("Connecting to database.")
        if psycopg2 is None:
            raise ValueError('Could not import psycopg2. Please install it.')

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
            self.con.autocommit = True  # prevents deadlocks
            self.cur = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        except Exception:
            self.logger.exception('Failed to connect to database.')
            self.stop()
        self.logger.info("Connected to PostgreSQL.")

        self.replace = self.parameters.replace_fields
        self.match = self.parameters.match_fields
        query = 'SELECT "{replace}" FROM "{table}" WHERE ' + 'AND '.join(['"{}" = %s '] * len(self.match))
        self.query = query.format(*self.match.values(),
                                  table=self.parameters.table,
                                  replace='", "'.join(self.replace.keys()))

    def process(self):
        event = self.receive_message()

        # Skip events with missing match-keys
        for key in self.match.keys():
            if key not in event:
                self.logger.debug('%s not present in event. Skipping event.', key)
                self.send_message(event)
                self.acknowledge_message()
                return

        # Skip events with existing data and overwrite is not allowed
        if all([key in event for key in self.replace.values()]) and not self.parameters.overwrite:
            self.send_message(event)
            self.acknowledge_message()
            return

        try:
            self.logger.debug('Executing %r.', self.cur.mogrify(self.query,
                                                                [event[key] for key in self.match.keys()]))
            self.cur.execute(self.query, [event[key] for key in self.match.keys()])
            self.logger.debug('Done.')
        except (psycopg2.InterfaceError, psycopg2.InternalError,
                psycopg2.OperationalError, AttributeError):
            self.logger.exception('Database connection problem, connecting again.')
            self.init()
        else:
            if self.cur.rowcount > 1:
                raise ValueError('Lookup returned more then one result. Please inspect.')
            elif self.cur.rowcount == 1:
                result = self.cur.fetchone()
                for key, value in self.replace.items():
                    event.add(value, result[key], overwrite=True)
                self.logger.debug('Applied.')
            else:
                self.logger.debug('No row found.')

            self.send_message(event)
            self.acknowledge_message()


BOT = GenericDBLookupExpertBot
