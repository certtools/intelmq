from copy import copy
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event


class CountryCodeFilterBot(Bot):
    
    def init(self):
        if not self.parameters.countrycode:
            self.cc = self.parameters.countrycode
            self.logger.warn("no country code found. countrycode_filter = %s" % self.parameters.countrycode)
            self.stop()
	else:
            self.logger.info("country code found. countrycode_filter = %s" % self.parameters.countrycode)

    def process(self):
        message = self.receive_message()

        if message:
            
            # Event deduplication
            if isinstance(message, Event):
		cc = message.contains("source_cymru_cc")
                if ( cc == self.cc ):
                    self.logger.debug("country code found! country = %s" % (cc))
                    self.send_message(message)
	self.acknowledge_message()


if __name__ == "__main__":
    bot = CountryCodeFilterBot(sys.argv[1])
    bot.start()
