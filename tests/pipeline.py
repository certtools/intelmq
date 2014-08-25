import redis
import time

class Pipeline():
    def __init__(self, source_queue, destination_queues, host="127.0.0.1", port="6379", db=2):
        
        self.source_queue = source_queue
        self.destination_queues = destination_queues
        
        self.redis = redis.Redis( host = host,
                                  port = int(port),
                                  db = db,
                                  socket_timeout = 5
                                )

    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def sleep(self, interval):
        time.sleep(interval)

    def send(self, message):
        for destination_queue in self.destination_queues:
            self.redis.lpush(destination_queue, message)

    def receive(self):
        return self.redis.lindex(self.source_queue, 0)
        
    def acknowledge(self):
        return self.redis.lpop(self.source_queue)