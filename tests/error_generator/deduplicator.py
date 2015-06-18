from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime
from intelmq.bots import utils


class DeduplicatorBot(Bot):
    
    def init(self):
        self.cache = Cache(
                            self.parameters.redis_cache_host,
                            self.parameters.redis_cache_port,
                            self.parameters.redis_cache_db,
                            self.parameters.redis_cache_ttl
                          )
        self.counter = 0
        self.lol_message = None

    def process(self):
        message = self.receive_message()
        message_hash = hash(message)

        if self.lol_message != message:
            self.counter += 1

        self.lol_message = message

        if self.counter == 10 or self.counter == 20:
            x = 10
            y = "20"
            z = x-y

        if not self.cache.exists(message_hash):
            self.cache.set(message_hash, 'hash')
            self.send_message(message)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = DeduplicatorBot(sys.argv[1])
    bot.start()
