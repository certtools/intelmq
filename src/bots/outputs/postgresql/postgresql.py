import sys
import psycopg2
import time
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

class PostgreSQLBot(Bot):



    def init(self):
        con = None
        try:    
            self.con = psycopg2.connect(
                                   database=self.parameters.database,
                                   user=self.parameters.user,
                                   #password=self.parameters.password,
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
            evdict = event.to_dict2()
            KEYS = ", ".join(evdict.keys())
            VALUES = evdict.values()
            FVALUES = len(VALUES) * "%s, "
            QUERY = "INSERT INTO logentry (" + KEYS + ") VALUES (" + FVALUES[:-2] + ")"
            try:
                self.cur.execute(QUERY, VALUES)

            except psycopg2.DatabaseError, e:
                print QUERY
                print VALUES
                print "\n\n"
                print e.pgerror
                self.logger.error("Postgresql Problem. Could not INSERT. Error: %s " % e.pgerror)
                time.sleep(5)
            self.con.commit()                                      
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot(sys.argv[1])
    bot.start()
