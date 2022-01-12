""" SQLMixin for IntelMQ

SPDX-FileCopyrightText: 2021 Birger Schacht
SPDX-License-Identifier: AGPL-3.0-or-later

Based on the former SQLBot base class
"""


class SQLMixin:
    """
    Inherit this bot so that it handles DB connection for you.
    You do not have to bother:
    * connecting database in the self.init() method, just call super().init(), self.cur will be set
    * catching exceptions, just call self.execute() instead of self.cur.execute()
    * self.format_char will be set to '%s' in PostgreSQL and to '?' in SQLite
    """

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    default_engine = "postgresql"
    engine = None
    # overwrite the default value from the OutputBot
    message_jsondict_as_string = True

    def __init__(self, *args, **kwargs):
        self.logger.debug("Running SQL Mixin initialization.")
        self.engine_name = getattr(self, 'engine', self.default_engine).lower()
        engines = {SQLMixin.POSTGRESQL: (self._init_postgresql, "%s"),
                   SQLMixin.SQLITE: (self._init_sqlite, "?")}
        for key, val in engines.items():
            if self.engine_name == key:
                val[0]()
                self.format_char = val[1]
                break
        else:
            raise ValueError("Wrong parameter 'engine' {0!r}, possible values are {1}".format(self.engine_name, engines))

        super().__init__()

    def _connect(self, engine, connect_args: dict, autocommitable: bool = False):
        self.engine = engine  # imported external library that connects to the DB
        self.logger.debug(f"Connecting to database with connect_args: {connect_args}.")

        try:
            self.con = self.engine.connect(**connect_args)
            if autocommitable:  # psycopg2 has it, sqlite3 has not
                self.con.autocommit = getattr(self, 'autocommit', True)  # True prevents deadlocks
            self.cur = self.con.cursor()
        except (self.engine.Error, Exception):
            self.logger.exception('Failed to connect to database.')
            self.stop()
        self.logger.info("Connected to database.")

    def _init_postgresql(self):
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError:
            raise exceptions.MissingDependencyError("psycopg2")

        self._connect(psycopg2,
                      {"database": self.database,
                       "user": self.user,
                       "password": self.password,
                       "host": self.host,
                       "port": self.port,
                       "sslmode": self.sslmode,
                       "connect_timeout": getattr(self, 'connect_timeout', 5)
                       },
                      autocommitable=True)

    def _init_sqlite(self):
        try:
            import sqlite3
        except ImportError:
            raise exceptions.MissingDependencyError("sqlite3")

        self._connect(sqlite3,
                      {"database": self.database,
                       "timeout": getattr(self, 'connect_timeout', 5)
                       }
                      )

    def execute(self, query: str, values: tuple, rollback=False):
        try:
            self.logger.debug('Executing %r.', (query, values))
            # note: this assumes, the DB was created with UTF-8 support!
            self.cur.execute(query, values)
            self.logger.debug('Done.')
        except (self.engine.InterfaceError, self.engine.InternalError,
                self.engine.OperationalError, AttributeError):
            if rollback:
                try:
                    self.con.rollback()
                    self.logger.exception('Executed rollback command '
                                          'after failed query execution.')
                except self.engine.OperationalError:
                    self.logger.exception('Executed rollback command '
                                          'after failed query execution.')
                    self.init()
                except Exception:
                    self.logger.exception('Cursor has been closed, connecting '
                                          'again.')
                    self.init()
            else:
                self.logger.exception('Database connection problem, connecting again.')
                self.init()
        else:
            return True
        return False
