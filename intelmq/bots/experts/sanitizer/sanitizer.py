from intelmq.lib.bot import Bot, sys
from intelmq.bots.utils import is_ip, is_domain_name, is_url, get_domain_name_from_url, get_ip_from_domain_name, get_ip_from_url

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            
            keys_pairs = [
                          ("source_ip", "source_domain_name", "source_url"),
                          ("destination_ip", "destination_domain_name", "destination_url")
                         ]

            for keys in keys_pairs:
            
                ip = domain_name = url = None
                
                for key in keys:
                    
                    reported_key = "reported_%s" % key
                    
                    if not event.contains(reported_key):
                        continue
                
                    value = event.value(reported_key)
                    
                    if len(value) <= 2: # ignore invalid values
                        continue
                
                    result = is_ip(value)
                    if result:
                        ip = result
                        
                    result = is_domain_name(value)
                    if result:
                        domain_name = result
                        
                    result = is_url(value)
                    if result:
                        url = result
                        
                if not domain_name and url:
                    domain_name = get_domain_name_from_url(url)

                if not ip and domain_name:
                    ip = get_ip_from_domain_name(domain_name)

                if not ip and url:
                    ip = get_ip_from_url(url)
                    
                for key in keys:
                    
                    if "url" in key and url:
                        event.add(key, url)
                        
                    if "domain_name" in key and domain_name:
                        event.add(key, domain_name)
                        
                    if "ip" in key and ip:
                        event.add(key, ip)
               
            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()

