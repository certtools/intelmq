# -*- coding: utf-8 -*-
import sys

from intelmq.lib.bot import Bot

import redis


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

        if event is None:
            self.acknowledge_message()
            return

        try:
            self.output.lpush(self.queue, event)
        except:
            self.logger.exception('Redis: failled to sent message!')
            self.connect()
        else:
            self.acknowledge_message()

    def connect(self):
        try:
            self.output = redis.StrictRedis(connection_pool=self.conn, socket_timeout=self.timeout, password=self.password)
            info = self.output.info()
        except redis.ConnectionError:
            self.logger.exception("Redis connection to {}:{} failed!!".format(self.host, self.port))
        else:
            self.logger.info("Connected successfully to Redis {} at {}:{}!".format(info['redis_version'], self.host, self.port))


if __name__ == "__main__":
    bot = RedisOutputBot(sys.argv[1])
    bot.start()
