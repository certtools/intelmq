import sys
import psycopg2
from lib.bot import *
from lib.utils import *
from lib.event import *

class PostgreSQLBot(Bot):

    def init(self):
        try:
            self.logger.debug("Connecting to PostgreSQL")
            self.con = psycopg2.connect(
                                   database=self.parameters.database,
                                   user=self.parameters.user,
                                   #password=self.parameters.password, # FIXME
                                   host=self.parameters.host,
                                   port=self.parameters.port
                                  )
            self.cur = self.con.cursor()
            self.logger.info("Connected to PostgreSQL")

        except psycopg2.DatabaseError, e:
            self.logger.error("Problem found when bot tried to connect to PostgreSQL. Error: %s " % e.pgerror)
            self.stop()


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
                self.logger.error("Problem found when bot tried to insert data into PostgreSQL. Error: %s " % e.pgerror)
                self.stop()
                
            self.con.commit()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot(sys.argv[1])
    bot.start()
