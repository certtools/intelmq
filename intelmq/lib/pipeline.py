# -*- coding: utf-8 -*-
import time
import warnings

import redis
from itertools import chain
from typing import Optional, Union

import intelmq.lib.exceptions as exceptions
import intelmq.lib.pipeline
import intelmq.lib.utils as utils

__all__ = ['Pipeline', 'PipelineFactory', 'Redis', 'Pythonlist', 'Amqp']

try:
    import pika
    try:
        import requests
    except ImportError:
        requests = None
except ImportError:
    pika = None


class PipelineFactory(object):

    @staticmethod
    def create(parameters: object, direction: Optional[str] = None,
               queues: Optional[Union[str, list, dict]] = None):
        """
        parameters: Parameters object
        direction: "source" or "destination", optional, needed for queues
        queues: needs direction to be set, calls set_queues
        """
        if direction not in [None, "source", "destination"]:
            raise exceptions.InvalidArgument("direction", got=direction,
                                             expected=["destination", "source"])
        if direction and hasattr(parameters, "%s_pipeline_broker" % direction):
            broker = getattr(parameters, "%s_pipeline_broker" % direction)
        else:
            if hasattr(parameters, 'broker'):
                broker = parameters.broker.title()
            else:
                broker = "Redis"
        pipe = getattr(intelmq.lib.pipeline, broker)(parameters)
        if queues and not direction:
            raise ValueError("Parameter 'direction' must be given when using "
                             "the queues parameter.")
        elif queues:
            pipe.set_queues(queues, direction)

        return pipe


class Pipeline(object):
    has_internal_queues = False

    def __init__(self, parameters):
        self.parameters = parameters
        self.destination_queues = {}  # type: dict of lists
        self.internal_queue = None
        self.source_queue = None

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def sleep(self, interval):
        warnings.warn("'Pipeline.sleep' will be removed in version 2.0.", DeprecationWarning)
        time.sleep(interval)

    def set_queues(self, queues, queues_type):
        """
        :param queues: For source queue, it's just string.
                    For destination queue, it can be one of the following:
                    None or list or dict (of strings or lists, one of the key should be '_default')

        :param queues_type: "source" or "destination"

        The method assures self.destination_queues are in the form of dict of lists. It doesn't assure there is a '_default' key.
        """
        if queues_type == "source":
            self.source_queue = queues
            if queues is not None:
                self.internal_queue = queues + "-internal"
            else:
                self.internal_queue = None

        elif queues_type == "destination":
            type_ = type(queues)
            if type_ is list:
                q = {"_default": queues}
            elif type_ is str:
                q = {"_default": queues.split()}
            elif type_ is dict:
                q = queues
                for key, val in queues.items():
                    q[key] = val if type(val) is list else val.split()
            else:
                raise exceptions.InvalidArgument(
                    'queues', got=queues,
                    expected=["None", "list of strings", "dict (of strings or lists that should have the _default key)"])
            self.destination_queues = q
        else:
            raise exceptions.InvalidArgument('queues_type', got=queues_type, expected=['source', 'destination'])

    def nonempty_queues(self) -> set:
        raise NotImplementedError


class Redis(Pipeline):
    has_internal_queues = True
    pipe = None

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

    def send(self, message, path="_default"):
        message = utils.encode(message)
        try:
            queues = self.destination_queues[path]
        except KeyError as exc:
            raise exceptions.PipelineError(exc)
        if self.load_balance:
            queues = [queues[self.load_balance_iterator]]
            self.load_balance_iterator += 1
            if self.load_balance_iterator == len(self.destination_queues[path]):
                self.load_balance_iterator = 0

        for destination_queue in queues:
            try:
                self.pipe.lpush(destination_queue, message)
            except Exception as exc:
                if 'Cannot assign requested address' in exc.args[0] or \
                        "OOM command not allowed when used memory > 'maxmemory'." in exc.args[0]:
                    raise MemoryError(exc.args[0])
                elif 'Redis is configured to save RDB snapshots, but is currently not able to persist on disk' in exc.args[0]:
                    raise IOError(28, 'No space left on device. Redis can\'t save its snapshots.')
                raise exceptions.PipelineError(exc)

    def receive(self):
        if self.source_queue is None:
            raise exceptions.ConfigurationError('pipeline', 'No source queue given.')
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
        queue_dict = {}
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

    def nonempty_queues(self) -> set:
        """ Returns a list of all currently non-empty queues. """
        if not self.pipe:
            self.set_queues(None, "source")
            self.connect()
        return {queue.decode() for queue in self.pipe.keys()}

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
        warnings.warn("'Pipeline.sleep' will be removed in version 2.0.", DeprecationWarning)

    def set_queues(self, queues, queues_type):
        super(Pythonlist, self).set_queues(queues, queues_type)
        self.state[self.internal_queue] = []
        self.state[self.source_queue] = []
        for destination_queue in chain.from_iterable(self.destination_queues.values()):
            self.state[destination_queue] = []

    def send(self, message, path="_default"):
        """Sends a message to the destination queues"""
        for destination_queue in self.destination_queues[path]:
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
        """
        if not self.state:
            self.set_queues(None, "source")
            self.connect()
        qdict = {}
        for queue in queues:
            qdict[queue] = len(self.state.get(queue, []))
        return qdict

    def clear_queue(self, queue):
        """ Empties given queue. """
        self.state[queue] = []


class Amqp(Pipeline):
    def __init__(self, parameters):
        super(Amqp, self).__init__(parameters)
        if pika is None:
            raise ValueError("To use AMQP you must install the 'pika' library.")
        self.properties = pika.BasicProperties(delivery_mode=2)  # message persistence

    def load_configurations(self, queues_type):
        self.host = getattr(self.parameters,
                            "{}_pipeline_host".format(queues_type),
                            "127.0.0.1")
        self.port = getattr(self.parameters,
                            "{}_pipeline_port".format(queues_type), 5672)
        self.username = getattr(self.parameters,
                                "{}_pipeline_username".format(queues_type),
                                None)
        self.password = getattr(self.parameters,
                                "{}_pipeline_password".format(queues_type),
                                None)
        #  socket_timeout is None by default, which means no timeout
        self.socket_timeout = getattr(self.parameters,
                                      "{}_pipeline_socket_timeout".format(
                                          queues_type),
                                      None)
        self.load_balance = getattr(self.parameters, "load_balance", False)
        self.virtual_host = getattr(self.parameters,
                                    "{}_amqp_virtual_host".format(queues_type),
                                    '/')
        self.load_balance_iterator = 0
        self.kwargs = {}
        if self.username and self.password:
            self.kwargs['credentials'] = pika.PlainCredentials(self.username, self.password)

    def connect(self, channelonly=False):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                            port=int(self.port),
                                                                            socket_timeout=self.socket_timeout,
                                                                            virtual_host=self.virtual_host,
                                                                            heartbeat=10,
                                                                            **self.kwargs,
                                                                            ))
        self.channel = self.connection.channel()
        if self.source_queue:
            self.channel.queue_declare(queue=self.source_queue, durable=True)
        for path in self.destination_queues.values():
            for destination_queue in path:
                self.channel.queue_declare(queue=destination_queue, durable=True)

    def disconnect(self):
        try:
            self.channel.close()
        except Exception:
            pass
        try:
            self.connection.close()
        except Exception:
            pass

    def set_queues(self, queues: dict, queues_type: str):
        self.load_configurations(queues_type)
        super(Amqp, self).set_queues(queues, queues_type)

    def _send(self, destination_queue, message):
        retval = False
        try:
            retval = self.channel.basic_publish(exchange='',
                                                routing_key=destination_queue,
                                                body=message,
                                                properties=self.properties,
                                                mandatory=True,
                                                )
        except Exception as exc:
            raise exceptions.PipelineError(exc)
        else:
            if not retval:
                raise exceptions.PipelineError('Sent message was not confirmed.')

    def send(self, message: str, path="_default"):
        """
        In principle we could use AMQP's exchanges here but that architecture is incompatible
        to the format of our pipeline.conf file.
        """
        message = utils.encode(message)
        try:
            queues = self.destination_queues[path]
        except KeyError as exc:
            raise exceptions.PipelineError(exc)
        if self.load_balance:
            queues = [queues[self.load_balance_iterator]]
            self.load_balance_iterator += 1
            if self.load_balance_iterator == len(self.destination_queues[path]):
                self.load_balance_iterator = 0

        for destination_queue in queues:
            self._send(destination_queue, message)

    def receive(self) -> str:
        if self.source_queue is None:
            raise exceptions.ConfigurationError('pipeline', 'No source queue given.')
        try:
            method, header, body = next(self.channel.consume(self.source_queue))
            if method:
                self.delivery_tag = method.delivery_tag
                return utils.decode(body)
        except Exception as exc:
            raise exceptions.PipelineError(exc)

    def acknowledge(self):
        try:
            self.channel.basic_ack(delivery_tag=self.delivery_tag)
        except pika.exceptions.ConnectionClosed:
            self.connect()
            self.channel.basic_ack(delivery_tag=self.delivery_tag)
        except Exception as e:
            raise exceptions.PipelineError(e)

    def count_queued_messages(self, *queues) -> dict:
        queue_dict = dict()
        for queue in queues:
            try:
                queue_dict[queue] = self.channel.queue_declare(queue=queue, passive=True).method.message_count
            except pika.exceptions.ChannelClosed as exc:  # channel not found and similar, need to re-declare
                if not exc.args or exc.args[0] in [404, 406]:
                    queue_dict[queue] = 0
                elif exc.args:
                    raise exceptions.PipelineError(exc)
                self.channel = self.connection.channel()
            except Exception as exc:
                raise exceptions.PipelineError(exc)
        return queue_dict

    def clear_queue(self, queue: str) -> bool:
        try:
            self.channel.queue_delete(queue=queue)
        except pika.exceptions.ChannelClosed as exc:  # channel not found and similar
            pass

    def nonempty_queues(self) -> set:
        if requests is False:
            return False
        try:
            result = requests.get('http://localhost:15672/api/queues', auth=('guest', 'guest'))
            if result:
                return {x['name'] for x in result.json() if x['messages']}
        except Exception:
            return False
