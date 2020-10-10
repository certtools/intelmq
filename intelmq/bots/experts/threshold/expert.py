# -*- coding: utf-8 -*-
"""Threshold value expert bot

SPDX-FileCopyrightText: 2020 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Given a stream of messages, this bot will let through only the single
one that makes the count of similar messages go above a threshold
value.

This bot is not multiprocessing safe. Do not run more than one
instance on the same Redis cache database.

Parameters:

    redis_cache_host: string

    redis_cache_port: int

    redis_cache_db: int

    redis_cache_password: string.  default: {None}

    filter_type: string ["whitelist", "blacklist"], when determining
                 whether two messages are similar, consider either
                 only the named fields, or all but the named fields
                 (time.observation is always ignored).

    bypass: boolean default: False

    filter_keys: list of strings, keys to exclude or include when
                 determining whether messages are similar.
                 time.observation is always ignored.

    threshold: int, number of messages after which one is sent on. As
               long as the count is above the threshold, no new
               messages will be sent.

    timeout: int, number of seconds to keep counts of similar
             messages. After this many seconds have elapsed, the count
             is deleted and "threshold" number of new messages will
             result in a new message being sent.

    add_keys: optional, array of strings to strings, keys to add to
              forwarded messages. Regardless of this setting, the
              field "extra.count" will be set to the number of
              messages seen (which will be the threshold value).

"""

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.exceptions import ConfigurationError


class ThresholdExpertBot(Bot):

    _message_processed_verb = 'Forwarded'

    is_multithreadable = False

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.timeout,
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )
        self.filter_keys = getattr(self.parameters, "filter_keys", [])
        self.filter_type = getattr(self.parameters, "filter_type", "whitelist")
        self.bypass = getattr(self.parameters, "bypass", False)
        self.timeout = getattr(self.parameters, "timeout", -1)
        if self.timeout <= 0:
            raise ConfigurationError('Timeout', 'Invalid timeout specified, use positive integer seconds.')
        self.threshold = getattr(self.parameters, "threshold", -1)
        if self.threshold <= 0:
            raise ConfigurationError('Threshold', 'Invalid threshold specified, use positive integer count.')
        self.add_keys = getattr(self.parameters, "add_keys", {})

    def process(self):
        message = self.receive_message()

        if self.bypass:
            self.send_message(message)
        else:
            message_hash = message.hash(filter_keys=self.filter_keys,
                                        filter_type=self.filter_type)
            old_count = int(self.cache.get(message_hash) or 0)
            self.logger.debug('Message %s has been seen %i times before.',
                              message_hash, old_count)
            # Use Redis "set" instead of "incr" to reset the timeout
            # every time
            self.cache.set(message_hash, str(old_count + 1))
            if old_count + 1 == self.threshold:
                self.logger.debug('Threshold reached, forwarding message.')
                message.update(self.add_keys)
                message.add('extra.count', old_count + 1, overwrite=True)
                self.send_message(message)
            else:
                self.logger.debug('Dropped message.')

        self.acknowledge_message()


BOT = ThresholdExpertBot
