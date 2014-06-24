import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *
import traceback
import json

class DebugBot(Bot):

    def process(self):
        event = self.pipeline.receive()
        
        if event:
            print unicode(event)
            self.pipeline.send(event)
        self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = DebugBot(sys.argv[1])
    bot.start()
