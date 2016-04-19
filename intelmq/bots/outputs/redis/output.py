# -*- coding: utf-8 -*-
import sys
import time
import redis
#import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class RedisOutputBot(Bot):

    def init(self)
        self.host = str(self.parameters.redis_server_ip)
        self.port = int(self.parameters.redis_server_port)
        self.db = int(self.parameters.redis_db)
        self.queue = str(self.parameters.redis_queue)
        self.password = str(self.parameters.redis_password)
        self.timeout = int(self.parameters.redis_timout)

        self.conn = redis.ConnectionPool(host = self.host, port = self.port, db = self.db)

    def process(self):
        event = self.receive_message()
        
        if event is None:
            self.acknowledge_message()
            return

        while True:
            try:
                output = redis.StrictRedis(connection_pool=self.conn, socket_timout=self.timeout, password=self.password)
                self.output.lpush(event.to_json)
                break
            except redis.ConnectionError:
                self.logger.error("Redis connection to {}:{} failed!! Retrying in 10 seconds".format(self.host,self.port))
                time.sleep(10)

        self.acknowledge_message()

if __name__ == "__main__":
    bot = RedisOutputBot(sys.argv[1])
    bot.start()
