from intelmq.lib.bot import Bot, sys
from intelmq.bots.experts.abusix.lib import Abusix

'''
Reference: https://abusix.com/contactdb.html
RIPE abuse contacts resolving through DNS TXT queries
'''


class AbusixExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            if event.contains(ip_key):
                ip = event.value(ip_key)
                email = Abusix.query(ip)
                if email:
                    abuse_contact_key = key + "abuse_contact"
                    event.add(abuse_contact_key, email)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AbusixExpertBot(sys.argv[1])
    bot.start()
