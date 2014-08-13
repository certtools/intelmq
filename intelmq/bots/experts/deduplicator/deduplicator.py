from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.event import Event

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

        if message:
            
            # Event deduplication
            if isinstance(message, Event):
                event = message
                event.clear("observation_time")
                message_hash = hash(event)                            

            # Generic message deduplication
            else:
                message_hash = hash(message)

            if not self.cache.exists(message_hash):
                self.send_message(message)
                self.cache.set(message_hash, 'hash')

        self.acknowledge_message()


if __name__ == "__main__":
    bot = DeduplicatorBot(sys.argv[1])
    bot.start()
