## MOVED into SQLBot - to be deleted

from intelmq.lib.bot import SQLBot

try:
    import sqlite3
except ImportError:
    sqlite3 = None


class SQLLiteBot(SQLBot):
    def init(self):
        super().init(sqlite3,
                     "sqlite3",
                     {"database": self.parameters.database,
                      "timeout": getattr(self.parameters, 'connect_timeout', 5)
                      }
                     )
