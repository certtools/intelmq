import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.harmonization import IPAddress
from intelmq.bots.experts.cymru_whois.lib import Cymru


MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128  # FIXME


class CymruExpertBot(Bot):

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           )

    def process(self):
        event = self.receive_message()

        keys = ["source.%s", "destination.%s"]

        for key in keys:
            ip_key = key % "ip"

            if not event.contains(ip_key):
                continue

            ip = event.value(ip_key)
            ip_version = IPAddress.version(ip)
            ip_integer = IPAddress.to_int(ip)

            if ip_version == 4:
                minimum = MINIMUM_BGP_PREFIX_IPV4

            elif ip_version == 6:
                minimum = MINIMUM_BGP_PREFIX_IPV6

            else:
                self.logger.error("Invalid IP version")
                self.send_message(event)
                self.acknowledge_message()

            cache_key = bin(ip_integer)[2: minimum + 2]
            result_json = self.cache.get(cache_key)

            if result_json:
                result = json.loads(result_json)
            else:
                result = Cymru.query(ip)
                result_json = json.dumps(result)
                self.cache.set(cache_key, result_json)

            if "asn" in result:
                event.add(key % 'asn', result['asn'], sanitize=True,
                          force=True)

            if "bgp_prefix" in result:
                event.add(key % 'bgp_prefix', result['bgp_prefix'],
                          sanitize=True, force=True)

            if "registry" in result:
                event.add(key % 'registry', result['registry'], sanitize=True,
                          force=True)

            if "allocated" in result:
                event.add(key % 'allocated', result['allocated'],
                          sanitize=True, force=True)

            if "as_name" in result:
                event.add(key % 'as_name', result['as_name'], sanitize=True,
                          force=True)

            if "cc" in result:
                event.add(key % 'geolocation.cc', result['cc'], sanitize=True,
                          force=True)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = CymruExpertBot(sys.argv[1])
    bot.start()
