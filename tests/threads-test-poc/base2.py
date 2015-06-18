import sys
import time
import redis
import threading
import Queue
from intelmq.bots.collectors.url.lib import fetch_url


# begin - IGNORE THIS CODE
def fill_it(xredis, queue):
    print "Fill source queue with %s messages." % MESSAGES_NUMBER
    for i in range(0, MESSAGES_NUMBER):
        message = "unknown message" + str(i)
        xredis.lpush(queue, message)

class StupidPipeline():

    def __init__(self):
        self.xredis = redis.Redis()
        self.source_queue = "mysource"

    def fill(self):
        fill_it(self.xredis, self.source_queue)

    def flush(self):
        self.xredis.flushall()


def get_url_content(url):
    try:
        return fetch_url(
                     url,
                     timeout = 60.0,
                     chunk_size = 16384,
                     http_proxy=None,
                     https_proxy=None
                    )
    except Exception, e:
        print e

# end - IGNORE THIS CODE







class Pipeline():

    def __init__(self):
        pool = redis.ConnectionPool(max_connections=10)
        self.xredis = redis.Redis(connection_pool=pool)

        self.source_queue = "mysource"
        self.internal_queue = "myinternal"
        self.destination_queue = "mydestination"
        
    def set_internal_queue(self):
        self.internal_queue = self.internal_queue

    def get_internal_queue(self):
        return self.internal_queue

    def fill(self):
        fill_it(self.xredis, self.source_queue)
        
    def flush(self):
        self.xredis.flushall()

    def receive(self):    
        return self.xredis.brpop(self.destination_queue)
            
    def acknowledge(self):
        self.xredis.rpop(self.destination_queue)

    def send(self, message):
        self.xredis.lpush(self.destination_queue, message)

class BotQueue():
        
    def start(self):
        pipe = Queue.Queue()   
        for thread_id in range(0, THREADS_NUMBER):
            thread = threading.Thread(target = self.process, args = (thread_id, pipe))
            thread.setDaemon(True)
            thread.start()

        size = 0
        while True:
            print pipe.get()
            size += 1
            if size == MESSAGES_NUMBER:
                break
        sys.exit(1)
    
    def process(self, thread_id, pipe):
        count = 1
        while True:
            data = None
            while not data:
                try:
                    data = get_url_content("http://127.0.0.1/head.txt")
                    pipe.put("thread:%s message-num:%s [%s]" % (str(thread_id), count, data.split()[0]))
                except:
                    data = None
                    time.sleep(0.2)
                count += 1        

class BotRedis():
        
    def start(self):
        pipe = Pipeline()
        for thread_id in range(0, THREADS_NUMBER):
            thread = threading.Thread(target = self.process, args = (thread_id, pipe))
            thread.setDaemon(True)
            thread.start()

        size = 0
        while True:
            print pipe.receive()[1]
            size += 1
            if size == MESSAGES_NUMBER:
                break
        sys.exit(1)
    
    def process(self, thread_id, pipe):
        count = 1
        while True:
            data = None
            while not data:
                try:
                    data = get_url_content("http://127.0.0.1/sample.txt")
                    pipe.send("thread:%s message-num:%s [%s]" % (str(thread_id), count, data.split()[0]))
                except:
                    data = None
                    time.sleep(1)
                count += 1




THREADS_NUMBER = 2
MESSAGES_NUMBER = 50
    
    
if __name__ == "__main__":
    if sys.argv[1] == "redis":
        bot = BotRedis()
    elif sys.argv[1] == "queue":
        bot = BotQueue()

    bot.start()
    
