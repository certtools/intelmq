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

        for key in ["source.%s", "destination.%s"]:
            geo_key = key % "geolocation.%s"

            ip = event.value(key % "ip")
            
            if not ip:
                continue
                
            try:
                info = self.database.city(ip)
            
                if info.country.iso_code:
                    event.clear(geo_key % "cc")
                    event.add(geo_key % "cc", unicode(info.country.iso_code))
                    
                if info.location.latitude:
                    event.clear(geo_key % "latitude")
                    event.add(geo_key % "latitude",  unicode(info.location.latitude))
                    
                if info.location.longitude:
                    event.clear(geo_key % "longitude")
                    event.add(geo_key % "longitude", unicode(info.location.longitude))
                    
                if info.city.name:
                    event.clear(geo_key % "city")
                    event.add(geo_key % "city", unicode(info.city.name))

            except geoip2.errors.AddressNotFoundError:
                pass
        
        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = GeoIPExpertBot(sys.argv[1])
    bot.start()
