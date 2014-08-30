import redis
import time

class Pipeline():
    def __init__(self, source_queue, destination_queues, host="127.0.0.1", port="6379", db=2):
        self.host = host
        self.port = port
        self.db = db
        
        if destination_queues and type(destination_queues) is not list:
            destination_queues = destination_queues.split()
        
        self.source_queue = source_queue
        if source_queue:
            self.internal_queue = source_queue + "-internal"
            
        self.destination_queues = destination_queues
        
        self.connect()

    def connect(self):
        self.redis = redis.Redis(
                          host = self.host,
                          port = int(self.port),
                          db = self.db,
                          socket_timeout = 50000
                        )
    
    def disconnect(self):
        pass
    
    def sleep(self, interval):
        time.sleep(interval)

    def send(self, message):
        for destination_queue in self.destination_queues:
            self.redis.rpush(destination_queue, message)

    def receive(self):
        try:
            # test if something after crash was stuck in internal queue
            return self.redis.brpoplpush(self.source_queue, self.internal_queue, 0)
        except redis.TimeoutError:
            self.connect()
            return self.redis.brpoplpush(self.source_queue, self.internal_queue, 0)
        
    def acknowledge(self):
        return self.redis.rpop(self.internal_queue)

# -----------------------
# Receive
# B RPOP LPUSH  source_queue  ->  source_queue_internal
# -----------------------
# Send
# LPUSH          object        ->  destination_queue
# -----------------------
# Acknowledge
# RPOP           object        <-  source_queue_internal
# -----------------------
