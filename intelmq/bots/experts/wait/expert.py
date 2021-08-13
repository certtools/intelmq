# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:25:58 2018

@author: sebastian
"""
import time

import redis

from intelmq.lib.bot import Bot


class WaitExpertBot(Bot):
    """Wait for a some time or until a queue size is lower than a given number"""
    queue_db: int = 2
    queue_host: str = "localhost"
    queue_name: str = None
    queue_password: str = None
    queue_polling_interval: float = 0.05
    queue_port: int = 6379
    queue_size: int = 0
    sleep_time: int = None

    def init(self):
        self.mode = None
        if self.queue_name:
            self.mode = 'queue'
            self.connect_redis()
        elif self.sleep_time:
            self.mode = 'sleep'
            self.sleep_time = float(self.sleep_time)
        else:
            self.mode = 'dummy'
        self.logger.debug('Wait mode is %s.', self.mode)

    def connect_redis(self):
        self.redis = redis.Redis(host=self.queue_host,
                                 port=self.queue_port,
                                 db=self.queue_db,
                                 password=self.queue_password,
                                 )

    def process(self):
        event = self.receive_message()
        if self.mode == 'queue':
            while self.redis.llen(self.queue_name) > self.queue_size:
                time.sleep(self.queue_polling_interval)
        elif self.mode == 'sleep':
            time.sleep(self.sleep_time)

        self.send_message(event)
        self.acknowledge_message()


BOT = WaitExpertBot
