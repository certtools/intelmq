import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.sanitize import *

class SanitizerBot(Bot):

    def process(self):
        event = self.pipeline.receive()

        if event:
            
            split_keys = ["ip", "url", "domain name", "email"]
            events = split_event_by_keys(event, split_keys)
            
            for event in events:
            
                event = sanitize_ip(event,
                    ("ip", "domain name"),
                    ("source ip", "source domain name"),
                    ("destination ip", "destination domain name"),
                    ("local ip", "local hostname")
                )

                event = sanitize_domain_name(event,
                    ("domain name", "ip"),
                    ("source domain name", "source ip"),
                    ("destination domain name", "destination ip"),
                    ("local hostname", "local ip")
                )
                
                event = sanitize_time(event, "source time")
                event = sanitize_time(event, "observation time")

                self.pipeline.send(event)
        self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()
