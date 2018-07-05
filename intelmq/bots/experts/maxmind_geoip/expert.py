# -*- coding: utf-8 -*-
"""
This product includes GeoLite2 data created by MaxMind, available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.
"""

from intelmq.lib.bot import Bot

try:
    import geoip2.database
except ImportError:
    geoip2 = None


class GeoIPExpertBot(Bot):

    def init(self):
        if geoip2 is None:
            raise ValueError('Could not import geoip2. Please install it.')

        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.exception("GeoIP Database does not exist or could not "
                                  "be accessed in %r.",
                                  self.parameters.database)
            self.logger.error("Read 'bots/experts/geoip/README' and follow the"
                              " procedure.")
            self.stop()
        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.%s", "destination.%s"]:
            geo_key = key % "geolocation.%s"

            if key % "ip" not in event:
                continue

            ip = event.get(key % "ip")

            try:
                info = self.database.city(ip)

                if info.country.iso_code:
                    event.add(geo_key % "cc", info.country.iso_code,
                              overwrite=self.parameters)

                if info.location.latitude:
                    event.add(geo_key % "latitude", info.location.latitude,
                              overwrite=self.parameters)

                if info.location.longitude:
                    event.add(geo_key % "longitude", info.location.longitude,
                              overwrite=self.parameters)

                if info.city.name:
                    event.add(geo_key % "city", info.city.name,
                              overwrite=self.parameters)

            except geoip2.errors.AddressNotFoundError:
                pass

        self.send_message(event)
        self.acknowledge_message()


BOT = GeoIPExpertBot
