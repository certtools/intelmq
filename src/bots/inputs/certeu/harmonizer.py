import sys
from lib.bot import *
from lib.utils import *
from lib.event import *


class CERTEUHarmonizerBot(Bot):
    
    def process(self):
        event = self.receive_message()
        if event:
            event.add("feed", "CERT-EU")
            event.add("taxonomy", "Malware")
            self.send_message(event)
            self.acknowledge_message()

if __name__ == "__main__":
    bot = CERTEUHarmonizerBot(sys.argv[1])
    bot.start()
