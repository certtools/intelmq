from intelmq.lib.bot import Bot, sys
from intelmq.bots import utils

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()
        print "--- RAW ---\n%s" % unicode(event)

        if event:
            
            keys_pairs = [
                            (
                                "source_ip",
                                "source_domain_name",
                                "source_url"
                            ),
                            (
                                "destination_ip",
                                "destination_domain_name",
                                "destination_url"
                            )
                        ]

            for keys in keys_pairs:
            
                ip = domain_name = url = None
                
                for key in keys:
                    
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
                    event.clear(key)
                    
                    if "url" in key and url:
                        event.add(key, url)
                        
                    if "domain_name" in key and domain_name:
                        event.add(key, domain_name)
                        
                    if "ip" in key and ip:
                        event.add(key, ip)
            
            print "\n\n--- COMPLETED ---\n%s" % unicode(event)
            raw_input("\n\n[ENTER]")
            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()

