# -*- coding: utf-8 -*-
import time

import redis

import intelmq.lib.exceptions as exceptions
import intelmq.lib.pipeline
import intelmq.lib.utils as utils

__all__ = ['Pipeline', 'PipelineFactory', 'Redis', 'Pythonlist']


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
            self.source_queue = queues
            if queues is not None:
                self.internal_queue = queues + "-internal"
            else:
                self.internal_queue = None

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
        self.password = getattr(self.parameters,
                                "{}_pipeline_password".format(queues_type),
                                None)
        #  socket_timeout is None by default, which means no timeout
        self.socket_timeout = getattr(self.parameters,
                                      "{}_pipeline_socket_timeout".format(
                                          queues_type),
                                      None)
        self.load_balance = getattr(self.parameters, "load_balance", False)
        self.load_balance_iterator = 0

    def connect(self):
        if self.host.startswith("/"):
            kwargs = {"unix_socket_path": self.host}

        elif self.host.startswith("unix://"):
            kwargs = {"unix_socket_path": self.host.replace("unix://", "")}

        else:
            kwargs = {
                "host": self.host,
                "port": int(self.port),
                "socket_timeout": self.socket_timeout,
            }

        self.pipe = redis.Redis(db=self.db, password=self.password, **kwargs)

    def disconnect(self):
        pass

    def set_queues(self, queues, queues_type):
        self.load_configurations(queues_type)
        super(Redis, self).set_queues(queues, queues_type)

    def send(self, message):
        message = utils.encode(message)
        if self.load_balance:
            destination_queue = self.destination_queues[
                self.load_balance_iterator]

            try:
                self.pipe.lpush(destination_queue, message)
            except Exception as exc:
                if 'Cannot assign requested address' in exc.args[0]:
                    raise MemoryError
                elif 'Redis is configured to save RDB snapshots, but is currently not able to persist on disk' in exc.args[0]:
                    raise IOError(28, 'No space left on device. Redis can\'t save its snapshots.')
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
        if self.source_queue is None:
            raise exceptions.ConfigurationError('pipeline', 'No source queue gievn.')
        try:
            retval = self.pipe.lindex(self.internal_queue, -1)  # returns None if no value
            if not retval:
                retval = self.pipe.brpoplpush(self.source_queue,
                                              self.internal_queue, 0)
            return utils.decode(retval)
        except Exception as exc:
            raise exceptions.PipelineError(exc)

    def acknowledge(self):
        try:
            return self.pipe.rpop(self.internal_queue)
        except Exception as e:
            raise exceptions.PipelineError(e)

    def count_queued_messages(self, *queues):
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
                self.state[destination_queue].append(utils.encode(message))
            else:
                self.state[destination_queue] = [utils.encode(message)]

    def receive(self):
        """
        Receives the last not yet acknowledged message.

        Does not block unlike the other pipelines.
        """
        if len(self.state.get(self.internal_queue, [])) > 0:
            return utils.decode(self.state[self.internal_queue].pop(0))

        first_msg = self.state[self.source_queue].pop(0)

        if self.internal_queue in self.state:
            self.state[self.internal_queue].append(first_msg)
        else:
            self.state[self.internal_queue] = [first_msg]

        return utils.decode(first_msg)

    def acknowledge(self):
        """Removes a message from the internal queue and returns it"""
        return self.state.get(self.internal_queue, [None]).pop(0)

    def count_queued_messages(self, *queues):
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
