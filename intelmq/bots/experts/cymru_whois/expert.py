# -*- coding: utf-8 -*-
import json

from intelmq.bots.experts.cymru_whois.lib import Cymru
from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.harmonization import IPAddress

MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128


class CymruExpertBot(Bot):

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )

    def process(self):
        event = self.receive_message()

        keys = ["source.%s", "destination.%s"]

        for key in keys:
            ip_key = key % "ip"

            if ip_key not in event:
                continue

            ip = event.get(ip_key)
            ip_version = IPAddress.version(ip)
            ip_integer = IPAddress.to_int(ip)

            if ip_version == 4:
                minimum = MINIMUM_BGP_PREFIX_IPV4

            elif ip_version == 6:
                minimum = MINIMUM_BGP_PREFIX_IPV6

            else:
                raise ValueError('Unexpected IP version '
                                 '{!r}.'.format(ip_version))

            cache_key = bin(ip_integer)[2: minimum + 2]
            result_json = self.cache.get(cache_key)

            if result_json:
                result = json.loads(result_json)
            else:
                result = Cymru.query(ip)
                if not result:
                    continue
                result_json = json.dumps(result)
                self.cache.set(cache_key, result_json)

            for result_key, result_value in result.items():
                event.add(key % result_key, result_value, overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = CymruExpertBot
