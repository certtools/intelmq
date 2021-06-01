# SPDX-FileCopyrightText: 2016 pedromreis
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import redis

from intelmq.lib.bot import Bot


class RedisOutputBot(Bot):
    """Send events to a Redis database"""
    hierarchical_output = False
    redis_db: int = 2
    redis_password: str = None
    redis_queue: str = None
    redis_server_ip = "127.0.0.1"
    redis_server_port = 6379
    redis_timeout = 5000
    with_type = True

    def init(self):
        self.host = self.redis_server_ip
        self.port = int(self.redis_server_port)
        self.db = int(self.redis_db)
        self.queue = self.redis_queue
        self.password = self.redis_password
        self.timeout = int(self.redis_timeout)

        redis_version = tuple(int(x) for x in redis.__version__.split('.'))
        if redis_version >= (3, 0, 0):
            self.redis_class = redis.Redis
        else:
            self.redis_class = redis.StrictRedis

        self.conn = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
        self.connect()

    def process(self):
        event = self.receive_message()

        try:
            self.output.lpush(self.queue,
                              event.to_json(hierarchical=self.hierarchical_output,
                                            with_type=self.with_type))
        except Exception:
            self.logger.exception('Failed to send message. Reconnecting.')
            self.connect()
        else:
            self.acknowledge_message()

    def connect(self):
        try:
            self.output = self.redis_class(connection_pool=self.conn, socket_timeout=self.timeout, password=self.password)
            info = self.output.info()
        except redis.ConnectionError:
            self.logger.exception("Redis connection to %s:%s failed!", self.host, self.port)
            self.stop()
        else:
            self.logger.info("Connected successfully to Redis %s at %s:%s!",
                             info['redis_version'], self.host, self.port)


BOT = RedisOutputBot
