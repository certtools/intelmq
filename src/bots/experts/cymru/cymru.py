import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *
from cymrulib import *

MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128 # FIXME

class CymruExpertBot(Bot):
    
    def init(self):
        self.cache = Cache(
                            self.parameters.cache_host,
                            self.parameters.cache_port,
                            self.parameters.cache_id,
                            self.parameters.cache_ttl
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
            
        ip, ip_version, ip_integer = is_ip(event.value("ip"))

        if not ip:
            self.send_message(event)
            self.acknowledge_message()
            return
        
        if ip_version == 4:
            cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV4 + 2]
        else:
            cache_key = bin(ip_integer)[2 : MINIMUM_BGP_PREFIX_IPV6 + 2]
        
        query_result = self.cache.get(cache_key)
        
        if not query_result:
            query_result = Cymru.query(ip, ip_version)
            self.cache.set(cache_key, query_result)
            
        asn, bgp, cc, registry, allocated, as_name = Cymru.parse(query_result)

        event.clear('cymru asn')
        event.clear('cymru bgp prefix')
        event.clear('cymru cc')
        event.clear('cymru registry')
        event.clear('cymru allocated')
        event.clear('cymru as name')

        event.add('cymru asn', asn)
        event.add('cymru bgp prefix', bgp)
        event.add('cymru cc', cc)
        event.add('cymru registry', registry)
        event.add('cymru allocated', allocated)
        event.add('cymru as name', as_name)

        self.send_message(event)
        self.acknowledge_message()
        
if __name__ == "__main__":
    bot = CymruExpertBot(sys.argv[1])
    bot.start()
