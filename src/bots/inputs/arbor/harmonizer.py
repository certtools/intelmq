import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

class ArborHarmonizerBot(Bot):

    def process(self):
        event = self.pipeline.receive()

        if event:
            event.add('feed', 'arbor')
            event.add('feed url', 'http://atlas-public.ec2.arbor.net/public/ssh_attackers')
            for value in event.values('ip'):
                event.add('source ip', value)
                event.add('reported ip', value)
            event.add('type', 'brute-force')
            
            self.pipeline.send(event)
        self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = ArborHarmonizerBot(sys.argv[1])
    bot.start()

