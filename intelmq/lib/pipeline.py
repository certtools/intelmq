import redis
import time


class Pipeline():
    def __init__(self, host="127.0.0.1", port="6379", db=2):
        self.host = host
        self.port = port
        self.db = db

        self.redis = redis.Redis(host=self.host,
                                 port=int(self.port),
                                 db=self.db,
                                 socket_timeout=50000)

    def set_source_queues(self, source_queue):
        """Sets the source queue of this pipeline"""
        self.source_queue = source_queue
        if source_queue:
            self.internal_queue = source_queue + "-internal"

    def set_destination_queues(self, destination_queues):
        """Sets the destination queues of this pipeline object"""
        if destination_queues and type(destination_queues) is not list:
            destination_queues = destination_queues.split()
        self.destination_queues = destination_queues

    def disconnect(self):
        """Disconnects from pipeline provider"""
        pass

    def sleep(self, interval):
        """Requests the pipeline to sleep for the given interval"""
        time.sleep(interval)

    def send(self, message):
        """Send given message on this pipeline object"""
        for destination_queue in self.destination_queues:
            self.redis.lpush(destination_queue, message)

    def receive(self):
        """Returns the last received message or
            any last message which wasn't yet acknowledged"""
        if self.redis.llen(self.internal_queue) > 0:
            return self.redis.lindex(self.internal_queue, -1)
        return self.redis.brpoplpush(self.source_queue, self.internal_queue, 0)

    def acknowledge(self):
        """Acknowledges the last received message
           and removes it from input queue """
        return self.redis.rpop(self.internal_queue)

    def count_queued_messages(self, queues):
        """Returns the amount of queued messages
           over all given queue names"""
        qdict = dict()
        for queue in queues:
            qdict[queue] = self.redis.llen(queue)
        return qdict


# Algorithm
# ---------
# [Receive]     B RPOP LPUSH   source_queue ->  internal_queue
# [Send]        LPUSH          message      ->  destination_queue
# [Acknowledge] RPOP           message      <-  internal_queue
