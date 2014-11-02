from intelmq.lib.bot import Bot, sys
from intelmq.bots.experts.ripencc.lib import RIPENCC

'''
Reference: https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=1.1.1.1

FIXME: Create a cache.

'''

class RIPENCCExpertBot(Bot):

    def process(self):

        event = self.receive_message()

        for key in ['source_','destination_']:
            if event.contains(key + "ip"):
                ip = event.value(key + "ip")
                email = RIPENCC.query(ip)
                if email:
                    event.add(key + "abuse_contact", email)

        self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = RIPENCCExpertBot(sys.argv[1])
    bot.start()
