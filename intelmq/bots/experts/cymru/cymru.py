import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.bots import utils
from intelmq.bots.experts.cymru.lib import Cymru

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

        keys = ["source_%s", "destination_%s"]
        
        for key in keys:
            ip = event.value(key % "ip")
            
            if not ip:
                self.send_message(event)
                self.acknowledge_message()
                return

            elif utils.is_ipv4(ip):
                ip_version = 4
                ip_integer = utils.ip_to_int(ip)
                cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV4 + 2]

            elif utils.is_ipv6(ip):
                ip_version = 6
                ip_integer = utils.ip_to_int(ip)
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
            
            if "asn" in result:
                event.clear(key % 'asn')
                event.add(key % 'asn',        result['asn'])
                
            if "bgp_prefix" in result:
                event.clear(key % 'bgp_prefix')
                event.add(key % 'bgp_prefix', result['bgp_prefix'])
                
            if "registry" in result:
                event.clear(key % 'registry')
                event.add(key % 'registry',   result['registry'])
                
            if "allocated" in result:
                event.clear(key % 'allocated')
                event.add(key % 'allocated',  result['allocated'])
                
            if "as_name" in result:
                event.clear(key % 'as_name')
                event.add(key % 'as_name',    result['as_name'])
                
            if "cc" in result:
                event.clear(key % 'cymru_cc')
                event.add(key % 'cymru_cc',   result['cc'])

        self.send_message(event)
        self.acknowledge_message()
        
if __name__ == "__main__":
    bot = CymruExpertBot(sys.argv[1])
    bot.start()
