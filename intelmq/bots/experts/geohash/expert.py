# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
    """Compute the geohash from longitude/latitude information, save it to extra.(source|destination)"""
    overwrite: bool = False
    precision: int = 7

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
                                     precision=self.precision),
                      overwrite=self.overwrite)

        self.send_message(event)
        self.acknowledge_message()


BOT = GeohashExpertBot
