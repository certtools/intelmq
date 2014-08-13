import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.bots.utils import is_ipv4, is_ipv6, ip_to_int
from cymrulib import Cymru

MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128 # FIXME

class CymruExpertBot(Bot):
    
    def init(self):
        self.cache = Cache(
                            self.parameters.redis_cache_host,
                            self.parameters.redis_cache_port,
                            self.parameters.redis_cache_db,
                            self.parameters.redis_cache_ttl
                          )

    
    def process(self):
        event = self.receive_message()
        
        if not event:
            self.acknowledge_message()
            return
            
        if not event.contains("ip"):
            self.send_message(event)
            self.acknowledge_message()
            return
        
        ip = event.value("ip")

        if is_ipv4(ip):
            ip_version = 4
            ip_integer = ip_to_int(ip)
            cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV4 + 2]

        elif is_ipv6(ip):
            ip_version = 6
            ip_integer = ip_to_int(ip)
            cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV6 + 2]

        else:
            self.send_message(event)
            self.acknowledge_message()
            return


        result_json = self.cache.get(cache_key)

        if result_json:
            result = json.loads(result_json)
        else:
            result = Cymru.query(ip, ip_version)
            result_json = json.dumps(result)
            self.cache.set(cache_key, result_json)
        
        event.clear('asn')
        event.clear('bgp_prefix')
        event.clear('registry')
        event.clear('allocated')
        event.clear('as_name')
        event.clear('cymru_cc')

        if "asn" in result:
            event.add('asn',        result['asn'])
            
        if "bgp_prefix" in result:
            event.add('bgp_prefix', result['bgp_prefix'])
            
        if "registry" in result:
            event.add('registry',   result['registry'])
            
        if "allocated" in result:
            event.add('allocated',  result['allocated'])
            
        if "as_name" in result:
            event.add('as_name',    result['as_name'])
            
        if "cc" in result:
            event.add('cymru_cc',   result['cc'])

        self.send_message(event)
        self.acknowledge_message()
        
if __name__ == "__main__":
    bot = CymruExpertBot(sys.argv[1])
    bot.start()
