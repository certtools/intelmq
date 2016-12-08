# -*- coding: utf-8 -*-

import redis

from intelmq.lib.bot import Bot


class RedisOutputBot(Bot):

    def init(self):
        self.host = self.parameters.redis_server_ip
        self.port = int(self.parameters.redis_server_port)
        self.db = int(self.parameters.redis_db)
        self.queue = self.parameters.redis_queue
        self.password = self.parameters.redis_password
        self.timeout = int(self.parameters.redis_timeout)

        self.conn = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.connect()

    def process(self):
        event = self.receive_message()

        try:
            self.output.lpush(self.queue, event)
        except:
            self.logger.exception('Failed to send message. Reconnecting.')
            self.connect()
        else:
            self.acknowledge_message()

    def connect(self):
        try:
            self.output = redis.StrictRedis(connection_pool=self.conn, socket_timeout=self.timeout, password=self.password)
            info = self.output.info()
        except redis.ConnectionError:
            self.logger.exception("Redis connection to {}:{} failed!!".format(self.host, self.port))
            self.stop()
        else:
            self.logger.info("Connected successfully to Redis {} at {}:{}!".format(info['redis_version'], self.host, self.port))


BOT = RedisOutputBot
