from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime
from intelmq.lib import utils


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
        message_hash = hash(message)

        if not self.cache.exists(message_hash):
            self.cache.set(message_hash, 'hash')
            self.send_message(message)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = DeduplicatorBot(sys.argv[1])
    bot.start()
