# -*- coding: utf-8 -*-
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache


class DeduplicatorExpertBot(Bot):

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           )

    def process(self):
        message = self.receive_message()

        ignore_keys = set(k.strip()
                          for k in self.parameters.ignore_keys.split(','))
        message_hash = message.hash(ignore_keys)

        old_hash = hash(int(message_hash, 16))

        if not (self.cache.exists(message_hash) or self.cache.exists(old_hash)):
            self.cache.set(message_hash, 'hash')
            self.send_message(message)
        else:
            self.logger.debug('Dropped message.')

        self.acknowledge_message()


if __name__ == "__main__":
    bot = DeduplicatorExpertBot(sys.argv[1])
    bot.start()
