from intelmq.lib.bot import Bot, sys
from intelmq.bots.experts.abusix.lib import Abusix

'''
Reference: https://abusix.com/contactdb.html
RIPE abuse contacts resolving through DNS TXT queries
'''

class AbusixExpertBot(Bot):

    def process(self):

        event = self.receive_message()

        for key in ['source_','destination_']:
            if event.contains(key + "ip"):
                ip = event.value(key + "ip")
                email = Abusix.query(ip)
                if email:
                    event.add(key + "abuse_contact", email)

        self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = AbusixExpertBot(sys.argv[1])
    bot.start()
