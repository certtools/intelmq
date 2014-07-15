import sys
from intelmq.lib.bot import *
from intelmq.lib.utils import *
from intelmq.lib.event import *
from intelmq.lib.cache import *
import traceback
import json

class DebugBot(Bot):

    def process(self):
        event = self.receive_message()
        
        if event:
            print unicode(event)
            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DebugBot(sys.argv[1])
    bot.start()
