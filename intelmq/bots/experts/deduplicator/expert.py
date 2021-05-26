# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""Deduplicator expert bot

Parameters:

    redis_cache_host: string

    redis_cache_port: int

    redis_cache_db: int

    redis_cache_ttl: int

    redis_cache_password: string.  default: {None}

    filter_type: string ["blacklist", "whitelist"]

    bypass: boolean default: False

    filter_keys: string with multiple keys separated by comma. Please
                 note that time.observation key is never consider by the
                 system because system will always ignore this key.
"""

from intelmq.lib.bot import Bot
from intelmq.lib.mixins import CacheMixin


class DeduplicatorExpertBot(Bot, CacheMixin):
    """Detection and drop exact duplicate messages. Message hashes are cached in the Redis database"""
    filter_keys: str = "raw,time.observation"  # TODO: could be List[str]
    filter_type: str = "blacklist"
    redis_cache_db: int = 6
    redis_cache_host: str = "127.0.0.1"  # TODO: could be ipaddress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 86400

    _message_processed_verb = 'Forwarded'
    bypass = False
    filter_keys = None

    def init(self):
        self.filter_keys = {k.strip() for k in
                            self.filter_keys.split(',')}

    def process(self):
        message = self.receive_message()

        if self.bypass:
            self.send_message(message)
        else:
            message_hash = message.hash(filter_keys=self.filter_keys,
                                        filter_type=self.filter_type)

            if not self.cache_exists(message_hash):
                self.cache_set(message_hash, 'hash')
                self.send_message(message)
            else:
                self.logger.debug('Dropped message.')

        self.acknowledge_message()


BOT = DeduplicatorExpertBot
