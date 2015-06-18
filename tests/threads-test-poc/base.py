import sys
import time
import redis
import threading

THREADS_NUMBER = 4
MESSAGES_NUMBER = 200


def fill_it(xredis, queue):
    print "Fill source queue with %s messages." % MESSAGES_NUMBER
    for i in range(0, MESSAGES_NUMBER):
        message = "unknown message" + str(i)
        xredis.lpush(queue, message)

   

class Pipeline():

    def __init__(self):
        self.xredis = redis.Redis()
        self.source_queue = "mysource"
        self.internal_queue = "myinternal"
        self.destination_queue = "mydestination"
        
    def fill(self):
        fill_it(self.xredis, self.source_queue)
        
    def flush(self):
        self.xredis.flushall()

    def receive(self):    
        #print "[+] Get message"
        return self.xredis.brpoplpush(self.source_queue, self.internal_queue, 0)

    def acknowledge(self):
        #print "[+] Acknowledge message"
        self.xredis.rpop(self.internal_queue)
        
    def send(self, message):
        #print "[+] Send message"
        self.xredis.lpush(self.destination_queue, message)
        
        
class Bot():
    
    def __init__(self, flush=False):
        if flush:
            cleaner = Pipeline()
            cleaner.flush()
            cleaner.fill()
        
    def start(self):
        for thread_id in range(0, THREADS_NUMBER):
            thread = threading.Thread(target = Bot.process, args = (thread_id,))
            thread.start()
    
    @staticmethod
    def process(thread_id):
        pipe = Pipeline()
        while True:
            message = pipe.receive()
            #time.sleep(0.5)
            pipe.send(message)
            print "Thread '%s' is sending message '%s'" % (thread_id, message)
            pipe.acknowledge()
        
    
    
if __name__ == "__main__":
    flush = False
    if len(sys.argv) == 2:
        flush = True
    bot = Bot(flush)
    bot.start()
    
