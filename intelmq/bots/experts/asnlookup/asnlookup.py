import pyasn
from intelmq.lib.bot import Bot, sys

class AsnLookupExpertBot(Bot):

    def init(self):
        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/asnlookup/README' and follow the procedure")
            self.stop()
    
    def process(self):
        event = self.receive_message()
        if event:
            
            keys = ["source_%s", "destination_%s"]
            
            for key in keys:
                ip = event.value(key % "ip")
                
                if not ip:
                    continue
                    
                try:
                    info = self.database.lookup(ip)
                
                    if info:
                        event.clear(key % "asn")
                        event.add(key % "asn", unicode(info[0]))
                        event.clear(key % "bgp_prefix")
                        event.add(key % "bgp_prefix", unicode(info[1]))
                        

                except Exception, e:
                    pass
            
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = AsnLookupExpertBot(sys.argv[1])
    bot.start()
