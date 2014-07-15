import sys
from intelmq.lib.bot import *
from intelmq.lib.utils import *
from intelmq.lib.event import *
from intelmq.lib.sanitize import *

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            
            # FIXME: BROKEN
            #split_keys = ["ip", "url", "domain name", "email"]
            #events = split_event_by_keys(event, split_keys)
            
            #for event in events:
            
            event = sanitize_ip(event,
                ("ip", "domain_name"),
                ("source_ip", "source_domain_name"),
                ("destination_ip", "destination_domain_name"),
                ("local_ip", "local_hostname")
            )

            event = sanitize_domain_name(event,
                ("domain_name", "ip"),
                ("source_domain_name", "source_ip"),
                ("destination_domain_name", "destination_ip"),
                ("local_hostname", "local_ip")
            )
            
            event = sanitize_time(event, "source_time")
            event = sanitize_time(event, "observation_time")

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()
