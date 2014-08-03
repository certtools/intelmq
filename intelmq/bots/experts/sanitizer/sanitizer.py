from intelmq.lib.bot import Bot, sys
from intelmq.lib import sanitize

class SanitizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:

            event = sanitize.ip(event,
                ("ip", "domain_name"),
                ("source_ip", "source_domain_name"),
                ("destination_ip", "destination_domain_name"),
                ("local_ip", "local_hostname")
            )

            event = sanitize.domain_name(event,
                ("domain_name", "ip"),
                ("source_domain_name", "source_ip"),
                ("destination_domain_name", "destination_ip"),
                ("local_hostname", "local_ip")
            )

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = SanitizerBot(sys.argv[1])
    bot.start()
