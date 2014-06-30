import sys
import geoip2.database

from lib.bot import *
from lib.utils import *
from lib.event import *

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
            ip = event.value("ip")
            if ip:
                event.clear("geoip cc")
                event.clear("city")
                event.clear("longitude")
                event.clear("latitude")

                info = self.database.city(ip)

                if info.country.iso_code:
                    event.add("geoip cc", info.country.iso_code)
                if info.location.latitude:
                    event.add("latitude",  str(info.location.latitude))
                if info.location.longitude:
                    event.add("longitude", str(info.location.longitude))
                if info.city.name:
                    event.add("city", info.city.name)
            
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = GeoIPExpertBot(sys.argv[1])
    bot.start()
