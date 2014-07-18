from intelmq.lib.bot import Bot, sys
from intelmq.lib.sanitize import sanitize_ip, sanitize_domain_name, sanitize_time

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:

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
