# -*- coding: utf-8 -*-
"""Deduplicator expert bot

Parameters:

    redis_cache_host: string

    redis_cache_port: int

    redis_cache_db: int

    redis_cache_ttl: int

    redis_cache_password: string.  default: {None}

    filter_type: string ["blacklist", "whitelist"]

    filter_keys: string with multiple keys separated by comma. Please
                 note that time.observation key is never consider by the
                 system because system will always ignore this key.
"""

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache


class DeduplicatorExpertBot(Bot):

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )
        self.filter_keys = set(k.strip() for k in
                               self.parameters.filter_keys.split(','))

    def process(self):
        message = self.receive_message()

        message_hash = message.hash(filter_keys=self.filter_keys,
                                    filter_type=self.parameters.filter_type)

        old_hash = hash(int(message_hash, 16))

        if not (self.cache.exists(message_hash) or self.cache.exists(old_hash)):
            self.cache.set(message_hash, 'hash')
            self.send_message(message)
        else:
            self.logger.debug('Dropped message.')

        self.acknowledge_message()


BOT = DeduplicatorExpertBot
