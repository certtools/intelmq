import redis
import time

class Pipeline():
    def __init__(self, source_queue, destination_queues, host="127.0.0.1", port="6379", db=2):
        
        if destination_queues and type(destination_queues) is not list:
            destination_queues = destination_queues.split()
        
        self.source_queue = source_queue
        if source_queue:
            self.internal_queue = source_queue + "-internal"
            
        self.destination_queues = destination_queues
        
        self.redis = redis.Redis( host = host,
                                  port = int(port),
                                  db = db,
                                  socket_timeout = 50000
                                )

    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def sleep(self, interval):
        time.sleep(interval)

    def send(self, message):
        for destination_queue in self.destination_queues:
            self.redis.rpush(destination_queue, message)

    def receive(self):
        #return self.redis.brpoplpush(self.source_queue, self.internal_queue, 0)
        return self.redis.lpop(self.source_queue)
        
    def acknowledge(self):
        pass
        #return self.redis.rpop(self.internal_queue)

# Receive
# B RPOP LPUSH  source_queue  ->  source_queue_internal

# Send
# LPUSH          object        ->  destination_queue

# Acknowledge
# RPOP           remove from 'source_queue_internal'
