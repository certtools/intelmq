# -*- coding: utf-8 -*-
"""
TODO: IPv6
"""
from __future__ import unicode_literals
import sys
import socket

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.harmonization import IPAddress

class ForwardDnsExpertBot(Bot):

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           )

    def process(self):
        event = self.receive_message()
        if event is None:
            self.acknowledge_message()
            return
        keys = ["source.%s", "destination.%s"]

        for key in keys:
            ip_key = key % "ip"
            fqdn_key = key % "fqdn"

            if event.contains(ip_key) or not event.contains(fqdn_key):
                continue

            fqdn = event[fqdn_key]
            cache_key = hash(fqdn)
            cachevalue = self.cache.get(cache_key)

            result = None
            if cachevalue:
                result = cachevalue
            else:
                soc = socket.getaddrinfo(fqdn, 0)
                try:
                    result = [address[4][0] for address in soc]                    
                except socket.error as msg:
                    print(msg)
                    continue
                else:
                    self.cache.set(cache_key, result)

            if result is not None:
                event.add(key % 'forward_dns',
                          "".join(result), sanitize=True, force=True)
        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ReverseDnsExpertBot(sys.argv[1])
    bot.start()
