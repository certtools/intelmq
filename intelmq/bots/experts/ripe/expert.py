# -*- coding: utf-8 -*-
import requests
import json

from intelmq.lib.bot import Bot


class RIPEExpertBot(Bot):

    def init(self):
        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.%s", "destination.%s"]:
            geo_key = key % "geolocation.%s"

            if key % "ip" not in event:
                continue

            ip = event.get(key % "ip")

            try:
                data = requests.get('https://stat.ripe.net/data/geoloc/data.json?resource=' + str(ip)).content
                info = (json.loads(data))['data']['locations'][0]

                if info['country']:
                    event.add(geo_key % "cc", info['country'].split('-')[0],
                              overwrite=self.overwrite)

                if info['latitude']:
                    event.add(geo_key % "latitude", info['latitude'],
                              overwrite=self.overwrite)

                if info['longitude']:
                    event.add(geo_key % "longitude", info['longitude'],
                              overwrite=self.overwrite)

                if info['city']:
                    event.add(geo_key % "city", info['city'],
                              overwrite=self.overwrite)

            except:
                pass

        self.send_message(event)
        self.acknowledge_message()


BOT = RIPEExpertBot
