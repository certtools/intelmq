# -*- coding: utf-8 -*-
"""
Aggregate Expert

SPDX-FileCopyrightText: 2021 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from datetime import datetime, timedelta
import time
import json
from intelmq.lib.bot import Bot
from intelmq.lib.utils import parse_relative
from intelmq.lib.mixins import CacheMixin


class AggregateExpertBot(Bot, CacheMixin):
    """Aggregation expert bot"""

    fields: str = "classification.type, classification.identifier"
    threshold: int = 10
    redis_cache_db: int = 8
    timespan: str = "1 hour"

    __timespan: int = 0
    __next_cleanup: int = 0

    def init(self):
        self.__timespan = parse_relative(self.timespan)
        self.fields = {k.strip() for k in self.fields.split(',')}
        self.cleanup()

    def cleanup(self):
        if self.__next_cleanup <= time.time():
            self.logger.debug('Started Cleanup.')
            delta = timedelta(minutes=self.__timespan)

            counter_sent = 0
            counter_ignored = 0
            counter_dropped = 0
            for key in self.cache_get_redis_instance().keys(pattern="aggregate.*"):
                keys = self.cache_get_redis_instance().hgetall(key)
                data = {y.decode('utf-8'): keys.get(y).decode('utf-8')
                        for y in keys.keys()}

                if datetime.now() <= (datetime.strptime(data['s'], '%Y-%m-%dT%H:%M:%S.%f') + delta):
                    counter_ignored += 1
                    continue

                if int(data['c']) >= self.threshold:
                    event = self.new_event(json.loads(data['d']))
                    event.add("time.source", data['s'])
                    event.add("extra.count", int(data['c']))
                    event.add("extra.time_end", data['l'])
                    self.send_message(event)
                    counter_sent += 1
                else:
                    counter_dropped += 1
                self.cache_get_redis_instance().delete(key)
            self.__next_cleanup = int(time.time()) + 10
            self.logger.debug('Completed Cleanup. Messages sent: %d, messages ignored: %d, messages dropped: %d.', counter_sent, counter_ignored, counter_dropped)
        else:
            self.logger.debug('Skipped Cleanup (%fs < 10s).', self.__next_cleanup - time.time())

    def process(self):
        event = self.receive_message()

        self.cleanup()

        message_hash = event.hash(filter_keys=self.fields, filter_type="whitelist")
        cache_id = f"aggregate.{message_hash}"

        if self.cache_exists(cache_id):
            # pipeline commands, because its faster to run them this way
            pipe = self.cache_get_redis_instance().pipeline()
            # set the last time we got an event to time.source/time.observation
            pipe.hset(name=cache_id, key="l", value=event.get('time.source') if event.get('time.source') else event.get('time.observation'))
            # count the count +1 up if no other extra.count is already given, else use extra.count as increment
            pipe.hincrby(name=cache_id, key="c", amount=int(event.get('extra.count', 1)))
            # execute the prepare commands
            pipe.execute(raise_on_error=True)
        else:
            # keys are shortened, to avoid high loads & unnecessary usage of ram
            # d = data
            # s = start time
            # f = first time
            # l = last time
            # c = count
            self.cache_get_redis_instance().hset(name=cache_id, mapping={
                'd': event.to_json(),
                's': datetime.now().isoformat(),
                'f': event.get('time.source') if event.get('time.source') else event.get('time.observation'),
                'l': event.get('time.source') if event.get('time.source') else event.get('time.observation'),
                'c': int(event.get('extra.count', 1))
            })

        self.acknowledge_message()


BOT = AggregateExpertBot
