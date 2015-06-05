import pyasn
from intelmq.lib.bot import Bot, sys

class ASNLookupExpertBot(Bot):

    def init(self):
        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/asnlookup/README' and follow the procedure")
            self.stop()
    
    def process(self):
        event = self.receive_message()
            
        keys = ["source_%s", "destination_%s"]
            
        for key in keys:
            ip = event.value(key % "ip")
            
            if not ip:
                continue
                
            info = self.database.lookup(ip)
        
            if info:
                if info[0]:
                    event.update(key % "asn", str(info[0]))
                if info[1]:
                    event.update(key % "bgp_prefix", str(info[1]))
            
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = ASNLookupExpertBot(sys.argv[1])
    bot.start()
