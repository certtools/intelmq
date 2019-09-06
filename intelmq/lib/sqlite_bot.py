from intelmq.lib.bot import SQLBot

try:
    import sqlite3
except ImportError:
    sqlite3 = None


class SQLLiteBot(SQLBot):
    def init(self):
        self.logger.debug("Connecting to database.")
        if sqlite3 is None:
            raise ValueError("Could not import 'sqlite3'. Please install it.")
        super().init(sqlite3, {"database": self.parameters.filename,
                               "timeout": getattr(self.parameters, 'connect_timeout', 5)
                               })
