import psycopg2
from intelmq.lib.bot import Bot, sys

class PostgreSQLBot(Bot):

    def init(self):
        try:
            self.logger.debug("Connecting to PostgreSQL")
            self.con = psycopg2.connect(
                                   database=self.parameters.database,
                                   user=self.parameters.user,
                                   password=self.parameters.password,
                                   host=self.parameters.host,
                                   port=self.parameters.port
                                  )
            self.cur = self.con.cursor()
            self.logger.info("Connected to PostgreSQL")

        except psycopg2.DatabaseError, e:
            self.logger.error("Problem found when bot tried to connect to PostgreSQL (%s)." % e)
            self.stop()


    def process(self):
        event = self.receive_message()
        if event:
            
            evdict  = event.to_dict()
            keys    = ", ".join(evdict.keys())
            values  = evdict.values()
            fvalues = len(values) * "%s, "
            query   = "INSERT INTO logentry (" + keys + ") VALUES (" + fvalues[:-2] + ")"
            
            try:
                self.cur.execute(query, values)
            except psycopg2.DatabaseError, e:
                self.logger.error("Problem found when bot tried to insert data into PostgreSQL (%s)." % e)
                self.stop()
                
            self.con.commit()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot(sys.argv[1])
    bot.start()
