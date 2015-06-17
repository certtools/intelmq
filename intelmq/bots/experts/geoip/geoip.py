import geoip2.database
from intelmq.lib.bot import Bot, sys

class GeoIPExpertBot(Bot):

    def init(self):
        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.error("GeoIP Database does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/geoip/README' and follow the procedure")
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
                    info = self.database.city(ip)
                
                    if info.country.iso_code:
                        event.clear(key % "cc")
                        event.add(key % "cc", unicode(info.country.iso_code))
                        
                    if info.location.latitude:
                        event.clear(key % "latitude")
                        event.add(key % "latitude",  unicode(info.location.latitude))
                        
                    if info.location.longitude:
                        event.clear(key % "longitude")
                        event.add(key % "longitude", unicode(info.location.longitude))
                        
                    if info.city.name:
                        event.clear(key % "city")
                        event.add(key % "city", unicode(info.city.name))

                except geoip2.errors.AddressNotFoundError:
                    pass
            
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = GeoIPExpertBot(sys.argv[1])
    bot.start()
