# -*- coding: utf-8 -*-
'''
Uses
https://pypi.org/project/geolib/
https://github.com/joyanujoy/geolib
'''
from intelmq.lib.bot import Bot

try:
    from geolib import geohash
except ImportError:
    geohash = None


class GeohashExpertBot(Bot):

    def init(self):
        if not geohash:
            raise ValueError("Library 'geolib' is required, please install it.")

    def process(self):
        event = self.receive_message()

        for key in ['source.geolocation.', 'destination.geolocation.']:
            latitude_key = key + "latitude"
            longitude_key = key + "longitude"
            geohash_key = "extra." + key + "geohash"
            if not (latitude_key in event and longitude_key in event):
                continue
            event.add(geohash_key,
                      geohash.encode(event[latitude_key],
                                     event[longitude_key],
                                     precision=self.parameters.precision),
                      overwrite=self.parameters.overwrite)

        self.send_message(event)
        self.acknowledge_message()


BOT = GeohashExpertBot
