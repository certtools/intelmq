# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import redis
import time
import zmq

import intelmq.lib.exceptions as exceptions
import intelmq.lib.pipeline
from intelmq import VAR_RUN_PATH


class PipelineFactory(object):

    @staticmethod
    def create(parameters):
        if hasattr(parameters, 'broker'):
            broker = parameters.broker.title()
        else:
            broker = "Redis"
        return getattr(intelmq.lib.pipeline, broker)(parameters)


class Pipeline(object):

    def __init__(self, parameters):
        self.parameters = parameters
        self.destination_queues = set()
        self.internal_queue = None
        self.source_queue = None

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def sleep(self, interval):
        time.sleep(interval)

    def set_queues(self, queues, queues_type):
        if queues_type == "source":
            self.source_queue = str(queues)
            self.internal_queue = str(queues) + "-internal"

        elif queues_type == "destination":
            if queues and type(queues) is not list:
                queues = queues.split()
            self.destination_queues = queues
        else:
            raise exceptions.InvalidArgument('queues_type', got=queues_type,
                                             expected=['source',
                                                       'destination'])


class Redis(Pipeline):

    def load_configurations(self, queues_type):
        self.host = getattr(self.parameters,
                            "{}_pipeline_host".format(queues_type),
                            "127.0.0.1")
        self.port = getattr(self.parameters,
                            "{}_pipeline_port".format(queues_type), "6379")
        self.db = getattr(self.parameters,
                          "{}_pipeline_db".format(queues_type), 2)
        self.socket_timeout = getattr(self.parameters,
                                      "{}_pipeline_socket_timeout".format(
                                          queues_type),
                                      50000)
        self.load_balance = getattr(self.parameters, "load_balance", False)
        self.load_balance_iterator = 0

    def connect(self):
        self.pipe = redis.Redis(host=self.host,
                                port=int(self.port),
                                db=self.db,
                                socket_timeout=self.socket_timeout
                                )

    def disconnect(self):
        pass

    def set_queues(self, queues, queues_type):
        self.load_configurations(queues_type)
        super(Redis, self).set_queues(queues, queues_type)

    def send(self, message):
        if self.load_balance:
            destination_queue = self.destination_queues[
                self.load_balance_iterator]

            try:
                self.pipe.lpush(destination_queue, message)
            except Exception as exc:
                raise exceptions.PipelineError(exc)

            self.load_balance_iterator += 1
            if self.load_balance_iterator == len(self.destination_queues):
                self.load_balance_iterator = 0

        else:
            for destination_queue in self.destination_queues:
                try:
                    self.pipe.lpush(destination_queue, message)
                except Exception as exc:
                    raise exceptions.PipelineError(exc)

    def receive(self):
        try:
            if self.pipe.llen(self.internal_queue) > 0:
                return self.pipe.lindex(self.internal_queue, -1)
            return self.pipe.brpoplpush(self.source_queue,
                                        self.internal_queue, 0)
        except Exception as e:
            raise exceptions.PipelineError(e)

    def acknowledge(self):
        try:
            return self.pipe.rpop(self.internal_queue)
        except Exception as e:
            raise exceptions.PipelineError(e)

    def count_queued_messages(self, queues):
        queue_dict = dict()
        for queue in queues:
            try:
                queue_dict[queue] = self.pipe.llen(queue)
            except Exception as exc:
                raise exceptions.PipelineError(exc)
        return queue_dict

    def clear_queue(self, queue):
        """Clears a queue by removing (deleting) the key,
        which is the same as an empty list in Redis"""
        try:
            return self.pipe.delete(queue)
        except Exception as exc:
            raise exceptions.PipelineError(exc)

# Algorithm
# ---------
# [Receive]     B RPOP LPUSH   source_queue ->  internal_queue
# [Send]        LPUSH          message      ->  destination_queue
# [Acknowledge] RPOP           message      <-  internal_queue


class Pythonlist(Pipeline):
    """
    This pipeline uses simple lists and is only for testing purpose.

    It behaves in most ways like a normal pipeline would do,
    but works entirely without external modules and programs.
    Data is saved as it comes (no conversion) and it is not blocking.
    """

    state = {}

    def connect(self):
        if self.parameters.raise_on_connect:
            raise exceptions.PipelineError('Connect failed as requested')

    def disconnect(self):
        pass

    def sleep(self, interval):
        pass

    def set_queues(self, queues, queues_type):
        super(Pythonlist, self).set_queues(queues, queues_type)
        self.state[self.internal_queue] = []
        self.state[self.source_queue] = []
        for destination_queue in self.destination_queues:
            self.state[destination_queue] = []

    def send(self, message):
        """Sends a message to the destination queues"""
        for destination_queue in self.destination_queues:
            if destination_queue in self.state:
                self.state[destination_queue].append(message)
            else:
                self.state[destination_queue] = [message]

    def receive(self):
        """
        Receives the last not yet acknowledged message.

        Does not block unlike the other pipelines.
        """
        if len(self.state.get(self.internal_queue, [])) > 0:
            return self.state[self.internal_queue].pop(0)

        first_msg = self.state[self.source_queue].pop(0)

        if self.internal_queue in self.state:
            self.state[self.internal_queue].append(first_msg)
        else:
            self.state[self.internal_queue] = [first_msg]

        return first_msg

    def acknowledge(self):
        """Removes a message from the internal queue and returns it"""
        return self.state.get(self.internal_queue, [None]).pop(0)

    def count_queued_messages(self, queues):
        """Returns the amount of queued messages
           over all given queue names.
           But only without a real message broker behind.
           As this is only for tests"""

        qdict = dict()
        for queue in queues:
            qdict[queue] = len(self.state.get(queue, []))
        return qdict

    def clear_queue(self, queue):
        """ Empties given queue. """
        self.state[queue] = []


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
        self.source_sock.bind("%s://%s%s.socket" % (self.communication,
                                                    VAR_RUN_PATH,
                                                    source_queue))

    def destination_queues(self, destination_queues, load_balance=False):
        # TODO: rename function
        # translate queues to port for tcp connecion
        # queues_translation = dict()
        if not destination_queues:
            return

        if destination_queues and type(destination_queues) is not list:
            destination_queues = destination_queues.split()

        self.dest_sock = []
        for destination_queue in destination_queues:
            sock = self.context.socket(zmq.PUSH)
            sock.connect("%s://%s%s.socket" % (self.communication,
                                               VAR_RUN_PATH,
                                               destination_queue))
            self.dest_sock.append(sock)

    def disconnect(self):
        raise NotImplementedError

    def sleep(self, interval):
        time.sleep(interval)

    def send(self, message):
        for sock in self.dest_sock:
            sock.send(message)  # TODO: send_string for unicode

    def receive(self):
        return self.source_sock.recv()

    def acknowledge(self):
        raise NotImplementedError

    def count_queued_messages(self, queues):
        raise NotImplementedError

    def clear_queue(self, queue):
        raise NotImplementedError
