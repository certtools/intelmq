from intelmq.lib.bot import Bot, sys
from intelmq.bots.utils import is_ip, is_domain_name, is_url, get_domain_from_url, get_ip_from_domain_name

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:

            # Add feature to ignore all values with just 3 characters in keys

            keys_pairs = [
                            ("source_ip", "source_domain_name", "source_url"),
                            ("destination_ip", "destination_domain_name", "destination_url")
                         ]
            
            for keys in keys_pairs:
            
                ip = domain_name = url = None
                
                for key in keys:
                    
                    if not event.contains(key):
                        continue
                
                    value = event.value(key)
                    event.discard(key)
                
                    result = is_ip(value)
                    if result:
                        ip = result
                        
                    result = is_domain_name(value)
                    if result:
                        domain_name = result
                        
                    result = is_url(value)
                    if result:
                        url = result
                        
                if not domain and url:
                    '''domain = get_domain_from_url(url)'''

                if not ip and domain:
                    '''ip = get_ip_from_domain_name(domain_name)'''
                    
                    
                for key in keys:
                    
                    if "url" in key:
                        event.add(key, url)
                        
                    if "domain_name" in key:
                        event.add(key, domain_name)
                        
                    if "ip" in key:
                        event.add(key, ip)


            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()

