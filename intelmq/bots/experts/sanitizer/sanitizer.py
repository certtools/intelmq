from intelmq.lib.bot import Bot, sys
from intelmq.bots import utils

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            
            keys_pairs = [
                            (
                                "source_ip",
                                "source_domain_name",
                                "source_url",
                                "source_asn"
                            ),
                            (
                                "destination_ip",
                                "destination_domain_name",
                                "destination_url",
                                "destination_asn"
                            )
                        ]

            for keys in keys_pairs:
            
                ip = domain_name = url = None
                
                for key in keys:
                    
                    if "asn" in key:
                        continue
                    
                    if not event.contains(key):
                        continue
                
                    value = event.value(key)
                    
                    if len(value) <= 2: # ignore invalid values
                        continue
                
                    result = utils.is_ip(value)
                    if result:
                        ip = result
                        
                    result = utils.is_domain_name(value)
                    if result:
                        domain_name = result
                        
                    result = utils.is_url(value)
                    if result:
                        url = result
                        
                if not domain_name and url:
                    domain_name = utils.get_domain_name_from_url(url)

                if not ip and domain_name:
                    ip = utils.get_ip_from_domain_name(domain_name)

                if not ip and url:
                    ip = utils.get_ip_from_url(url)
                    
                for key in keys:
                    
                    if "url" in key and url:
                        event.clear(key)
                        event.add(key, url)
                        
                    if "domain_name" in key and domain_name:
                        event.clear(key)
                        event.add(key, domain_name)
                        
                    if "ip" in key and ip:
                        event.clear(key)
                        event.add(key, ip)

                    if "asn" in key:
                        try:
                            int(event.value(key))
                        except:
                            event.clear(key)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()

