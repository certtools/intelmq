## MOVED into SQLBot - to be deleted

from intelmq.lib.bot import SQLBot

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None


class PostgreSQLBot(SQLBot):
    def init(self):
        super().init(psycopg2,
                     "psycopg2",
                     {"database": self.parameters.database,
                      "user": self.parameters.user,
                      "password": self.parameters.password,
                      "host": self.parameters.host,
                      "port": self.parameters.port,
                      "sslmode": self.parameters.sslmode,
                      "connect_timeout": getattr(self.parameters, 'connect_timeout', 5)
                      },
                     {"cursor_factory": psycopg2.extras.RealDictCursor},
                     autocommitable=True)
