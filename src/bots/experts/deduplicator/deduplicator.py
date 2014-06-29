import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *
import traceback

''' Deduplicato
    System check if it already saw a specific message using Redias as memcache
'''

class DeduplicatorBot(Bot):

    def process(self):
        message = self.receive_message()

        if message:
            message_hash = hash(message)

            if not self.cache.exists(message_hash):
                self.send_message(message)
                self.cache.set(message_hash, 'hash')
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DeduplicatorBot(sys.argv[1])
    bot.start()
