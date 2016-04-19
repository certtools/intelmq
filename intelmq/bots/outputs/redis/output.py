# -*- coding: utf-8 -*-
import sys
import time
import redis
import intelmq.lib.utils as utils
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
        
        if event is None:
            self.acknowledge_message()
            return

        while True:
            try:
                self.output.lpush(self.queue, utils.encode(event.to_json()))
                break
            except redis.RedisError as e:
                self.logger.error('Redis: failled to sent message!')
                self.logger.error(e)
                self.connect()

        self.acknowledge_message()
    
    def connect(self):
        while True:
            try:
                self.output = redis.StrictRedis(connection_pool=self.conn, socket_timeout=self.timeout, password=self.password)
                info = self.output.info()
                break
            except redis.ConnectionError as e:
                self.logger.error("Redis connection to {}:{} failed!! Retrying in 10 seconds".format(self.host,self.port))
                self.logger.error(e)
                time.sleep(10)
        self.logger.info("Connected successfully to Redis {} at {}:{}!".format(info['redis_version'], self.host,self.port))

if __name__ == "__main__":
    bot = RedisOutputBot(sys.argv[1])
    bot.start()
