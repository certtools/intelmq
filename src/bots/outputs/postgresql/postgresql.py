import sys
import psycopg2
from lib.bot import *
from lib.utils import *
from lib.event import *

class PostgreSQLBot(Bot):

    def init(self):
        con = None
        try:    
            self.con = psycopg2.connect(
                                   database=self.parameters.database,
                                   user=self.parameters.user,
                                   #password=self.parameters.password, # FIXME
                                   host=self.parameters.host,
                                   port=self.parameters.port
                                  )
            self.logger.info("info: con = %r" %self.con)

        except psycopg2.DatabaseError, e:
            self.logger.error("Postgresql Problem. Could not connect to the database. Error: %s " % e.pgerror)
            self.stop()
        self.cur = self.con.cursor() 


    def process(self):
        event = self.receive_message()
        
        if event:
            evdict = event.to_dict2()  # FIXME: rename the method or use to_dict()
            KEYS = ", ".join(evdict.keys())
            VALUES = evdict.values()
            FVALUES = len(VALUES) * "%s, "
            QUERY = "INSERT INTO logentry (" + KEYS + ") VALUES (" + FVALUES[:-2] + ")"
            try:
                self.cur.execute(QUERY, VALUES)
            except psycopg2.DatabaseError, e:
                # FIXME: try to use the try:except from start method at lib/bot.py
                self.logger.error("Postgresql Problem. Could not INSERT. Error: %s " % e.pgerror)
            self.con.commit()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot(sys.argv[1])
    bot.start()
