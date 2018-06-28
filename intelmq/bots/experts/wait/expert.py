# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:25:58 2018

@author: sebastian
"""
import redis
import time

from intelmq.lib.bot import Bot


class WaitExpertBot(Bot):
    def init(self):
        self.mode = None
        self.queue_name = getattr(self.parameters, 'queue_name', None)
        self.sleep_time = getattr(self.parameters, 'sleep_time', None)
        if self.queue_name:
            self.mode = 'queue'
            self.queue_db = int(getattr(self.parameters, 'queue_db', 2))
            self.queue_host = getattr(self.parameters, 'queue_host', 'localhost')
            self.queue_password = getattr(self.parameters, 'queue_password', None)
            self.queue_polling_interval = float(getattr(self.parameters, 'queue_polling_interval', 0.05))
            self.queue_port = int(getattr(self.parameters, 'queue_port', 6379))
            self.queue_size = int(getattr(self.parameters, 'queue_size', 0))
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
