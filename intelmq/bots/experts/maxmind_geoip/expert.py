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

            if not event.contains(key % "ip"):
                continue
                
            ip = event.value(key % "ip")
                
            try:
                info = self.database.city(ip)
            
                if info.country.iso_code:
                    event.add(geo_key % "cc", info.country.iso_code, sanitize=True, force=True)
                    
                if info.location.latitude:
                    event.add(geo_key % "latitude", unicode(info.location.latitude), sanitize=True, force=True)
                    
                if info.location.longitude:
                    event.add(geo_key % "longitude", unicode(info.location.longitude), sanitize=True, force=True)
                    
                if info.city.name:
                    event.add(geo_key % "city", info.city.name, sanitize=True, force=True)

            except geoip2.errors.AddressNotFoundError:
                pass
        
        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = GeoIPExpertBot(sys.argv[1])
    bot.start()
