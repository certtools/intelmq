import sys
import geoip2.database

from lib.bot import *
from lib.utils import *
from lib.event import *

class GeoIPExpertBot(Bot):

    def __init__(self, bot_id):
        super(GeoIPExpertBot, self).__init__(bot_id)
        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.error("GeoIP Database does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/geoip/README' and follow the procedure")
            self.exit()
    
    def process(self):
        event = self.receive_message()
        if event:
            ip = event.value("ip")
            ip_cc = self.database.city(ip)
            event.add("geoip cc", ip_cc.country.iso_code)
            event.add("geoip latitude",  str(ip_cc.location.latitude))
            event.add("geoip longitude", str(ip_cc.location.longitude))
            if ip_cc.city.name:
                event.add("geoip city", ip_cc.city.name)
            
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = GeoIPExpertBot(sys.argv[1])
    bot.start()
