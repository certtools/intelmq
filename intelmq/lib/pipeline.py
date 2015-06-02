import redis
import zmq
import time
import intelmq.lib.pipeline
import intelmq.lib.exceptions as exceptions
from intelmq import VAR_RUN_PATH

class PipelineFactory(object):
    
    @staticmethod
    def create(parameters):
        try:
            if hasattr(parameters, 'broker'):
                class_reference = getattr(intelmq.lib.pipeline, parameters.broker.title())
            else:
                class_reference = getattr(intelmq.lib.pipeline, "Redis")
            return class_reference(parameters)
        except TypeError:
            raise  exceptions.PipelineFactoryError("No broker specified for the pipeline") # FIXME: change raise message


class Pipeline():

    def __init__(self):
        pass

    def connect(self):
        pass # FIXME: raise

    def disconnect(self):
        pass # FIXME: raise

    def sleep(self, interval):
        time.sleep(interval)
        

class Redis(Pipeline):

    def __init__(self, parameters):
        self.parameters = parameters


    def load_configurations(self, queues_type):
        self.host = getattr(self.parameters, "%s_pipeline_host" % (queues_type), "127.0.0.1")
        self.port = getattr(self.parameters, "%s_pipeline_port" % (queues_type), "6379")
        self.db = getattr(self.parameters, "%s_pipeline_db" % (queues_type), 2)
        self.socket_timeout = getattr(self.parameters, "%s_pipeline_socket_timeout" % (queues_type), 50000)
        self.load_balance = getattr(self.parameters, "load_balance", False)
        self.load_balance_iterator = 0


    def connect(self):
        self.pipe = redis.Redis(
                                 host = self.host,
                                 port = int(self.port),
                                 db = self.db,
                                 socket_timeout = self.socket_timeout
                               )


    def disconnect(self):
        pass


    def set_queues(self, queues, queues_type):
        self.load_configurations(queues_type)

        if queues_type == "source":
            self.source_queue = str(queues)
            self.internal_queue = str(queues) + "-internal"

        elif queues_type == "destination":
            if queues and type(queues) is not list:
                queues = queues.split()     
            self.destination_queues = queues
        else:
            pass # FIXME: raise
    

    def send(self, message):
        if self.load_balance:
            destination_queue = self.destination_queues[self.load_balance_iterator]

            try:
                self.pipe.lpush(destination_queue, message)
            except Exception, e:
                raise exceptions.PipelineError(e)

            self.load_balance_iterator += 1
            if self.load_balance_iterator == len(self.destination_queues):
                self.load_balance_iterator = 0

        else:
            for destination_queue in self.destination_queues:
                try:
                    self.pipe.lpush(destination_queue, message)
                except Exception, e:
                    raise exceptions.PipelineError(e)


    def receive(self):
        try:
            if self.pipe.llen(self.internal_queue) > 0:
                return self.pipe.lindex(self.internal_queue, -1)
            return self.pipe.brpoplpush(self.source_queue, self.internal_queue, 0)
        except Exception, e:
            raise exceptions.PipelineError(e)
        

    def acknowledge(self):
        try:
            return self.pipe.rpop(self.internal_queue)
        except Exception, e:
            raise exceptions.PipelineError(e)


    def count_queued_messages(self, queues):
        queue_dict = dict()
        for queue in queues:
            try:
                queue_dict[queue] = self.pipe.llen(queue)
            except Exception, e:
                raise exceptions.PipelineError(e)
        return queue_dict

# Algorithm
# ---------
# [Receive]     B RPOP LPUSH   source_queue ->  internal_queue
# [Send]        LPUSH          message      ->  destination_queue
# [Acknowledge] RPOP           message      <-  internal_queue



class Zeromq(Pipeline):
    
    def __init__(self, host="127.0.0.1", communication="ipc"):
        
        # ZeroMQ Context
        self.context = zmq.Context()
        self.host = host
        self.communication = communication
        
        
    def source_queues(self, source_queue):
        # translate queues to port for tcp connecion
        # queues_translation = dict()

        self.source_sock = self.context.socket(zmq.PULL)
        self.source_sock.bind("%s://%s%s.socket" % (self.communication, VAR_RUN_PATH, source_queue) )
        
    def destination_queues(self, destination_queues, load_balance):
        # translate queues to port for tcp connecion
        # queues_translation = dict()
        if not destination_queues:
            return
        
        if destination_queues and type(destination_queues) is not list:
            destination_queues = destination_queues.split()

        self.dest_sock = []
        for destination_queue in destination_queues:
            sock = self.context.socket(zmq.PUSH)
            sock.connect("%s://%s%s.socket" % (self.communication, VAR_RUN_PATH, destination_queue))
            self.dest_sock.append(sock)
        
    def disconnect(self):
        pass
    
    def sleep(self, interval):
        time.sleep(interval)

    def send(self, message):
        for sock in self.dest_sock:
            sock.send(message)

    def receive(self):
        return self.source_sock.recv()

    def acknowledge(self):
        pass

    def count_queued_messages(self, queues):
        return 0
        #pass
        
    

