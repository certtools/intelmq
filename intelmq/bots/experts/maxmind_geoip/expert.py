# -*- coding: utf-8 -*-

from intelmq.lib.bot import Bot

try:
    import geoip2.database
except ImportError:
    geoip2 = None


class GeoIPExpertBot(Bot):

    def init(self):
        if geoip2 is None:
            self.logger.error('Could not import geoip2. Please install it.')
            self.stop()

        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.exception("GeoIP Database does not exist or could not "
                                  "be accessed in {}"
                                  "".format(self.parameters.database))
            self.logger.error("Read 'bots/experts/geoip/README' and follow the"
                              " procedure")
            self.stop()

    def process(self):
        event = self.receive_message()

        for key in ["source.%s", "destination.%s"]:
            geo_key = key % "geolocation.%s"

            if not event.contains(key % "ip"):
                continue

            ip = event.get(key % "ip")

            try:
                info = self.database.city(ip)

                if info.country.iso_code:
                    event.add(geo_key % "cc", info.country.iso_code,
                              force=True)

                if info.location.latitude:
                    event.add(geo_key % "latitude", info.location.latitude,
                              force=True)

                if info.location.longitude:
                    event.add(geo_key % "longitude", info.location.longitude,
                              force=True)

                if info.city.name:
                    event.add(geo_key % "city", info.city.name, force=True)

            except geoip2.errors.AddressNotFoundError:
                pass

        self.send_message(event)
        self.acknowledge_message()


BOT = GeoIPExpertBot
