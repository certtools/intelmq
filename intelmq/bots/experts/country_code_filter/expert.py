from copy import copy
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event


class CountryCodeFilterBot(Bot):
    
    def init(self):
        if not self.parameters.countrycode:
            self.logger.warn("no country code found. countrycode_filter = %s" % self.parameters.countrycode)
            self.stop()
        else:
            self.logger.info("country code found. countrycode_filter = %s" % self.parameters.countrycode)

    def process(self):
        event = self.receive_message()

        for key in ["source.geolocation.cc", "destination.geolocation.cc"]:
            if event.contains(key):
                if self.parameters.countrycode == event.value(key):
                    self.send_message(message)
                    break

        self.acknowledge_message()


if __name__ == "__main__":
    bot = CountryCodeFilterBot(sys.argv[1])
    bot.start()
