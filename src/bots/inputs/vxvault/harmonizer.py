#!/usr/bin/python

import sys
import urlparse
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *
import time

class VXVaultHarmonizerBot(Bot):

    def process(self):
        event = self.pipeline.receive()
        
        if event:
            event.add('feed', 'vxvault')
            event.add('feed url', 'http://vxvault.siri-urz.net/URL_List.php')
            for value in event.values('ip'):
                event.add('source ip', value)
                event.add('reported ip', value)
            event.add('type', 'malware')

            self.pipeline.send(event)
        self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = VXVaultHarmonizerBot(sys.argv[1])
    bot.start()
