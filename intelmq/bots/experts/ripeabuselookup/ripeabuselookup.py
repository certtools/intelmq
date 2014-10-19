from intelmq.lib.bot import Bot, sys
from intelmq.bots.experts.ripeabuselookup.lib import RIPENCC


'''
Reference: https://stat.ripe.net/data/abuse-contact-finder/data.json?resource=1.1.1.1

Be careful, sometimes there is no response when there is no abuse_c field in RIPE
FIXME: create cache! Lookups are sloooowwww....

'''

class ripeabuselookup(Bot):


    def init(self):
	pass
    
    def process(self):
        event = self.receive_message()
        if event:
            if event.contains("source_ip") and event.contains("source_registry") and event.value("source_registry") == "ripencc":
		ip = event.value("source_ip")
		email = None
		email = RIPENCC.query(ip, "ipv4")
		if (None != email):
			event.add("abuse_contact",email)
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = ripeabuselookup(sys.argv[1])
    bot.start()
