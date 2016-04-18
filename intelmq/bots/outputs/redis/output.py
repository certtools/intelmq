# -*- coding: utf-8 -*-
import sys
import time
import redis
import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class RedisOutputBot(Bot):

    def init(self)
        self.destination_queue = self.parameters.redis_queue
        self.conn = redis.ConnectionPool(host=self.parameters.redis_server_ip, 
                                         port=int(self.parameters.redis_server_port), 
                                         int(self.parameters.redis_db)
                                        )

    def process(self):
        event = self.receive_message()
        
        if event is None:
            self.acknowledge_message()
            return

        while True:
            try:
                output = redis.Redis(connection_pool=self.conn)
                self.output.lpush(event.to_json)
                break
            except redis.ConnectionError:
                self.logger.error("Redis connection failled, retrying in 10 seconds")
                time.sleep(10)

        self.acknowledge_message()

if __name__ == "__main__":
    bot = RedisOutputBot(sys.argv[1])
    bot.start()
