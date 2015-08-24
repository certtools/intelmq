import sys

from intelmq.bots.experts.ripencc.lib import RIPENCC
from intelmq.lib.bot import Bot


'''
Reference: https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=1.1.1.1

TODO:
Load RIPE networks prefixes into memory.
Compare each IP with networks prefixes loadad.
If ip matchs, query RIPE
'''


class RIPENCCExpertBot(Bot):

    def process(self):

        event = self.receive_message()

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            if event.contains(ip_key):
                ip = event.value(ip_key)
                email = RIPENCC.query(ip)
                if email:
                    event.add(key + "abuse_contact", email, sanitize=True)

        self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = RIPENCCExpertBot(sys.argv[1])
    bot.start()
