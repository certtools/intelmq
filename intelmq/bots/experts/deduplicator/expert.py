import copy
import json
from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache


class DeduplicatorBot(Bot):
    
    def init(self):
        self.cache = Cache(
                            self.parameters.redis_cache_host,
                            self.parameters.redis_cache_port,
                            self.parameters.redis_cache_db,
                            self.parameters.redis_cache_ttl
                          )

    def process(self):
        message = self.receive_message()
        auxiliar_message = copy.copy(message)

        ignore_keys = self.parameters.ignore_keys.split(',')

        for ignore_key in ignore_keys:
            ignore_key = ignore_key.strip()
            auxiliar_message.clear(ignore_key)        

        message_hash = hash(auxiliar_message)

        if not self.cache.exists(message_hash):
            self.cache.set(message_hash, 'hash')
            self.send_message(message)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = DeduplicatorBot(sys.argv[1])
    bot.start()
