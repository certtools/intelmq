# -*- coding: utf-8 -*-
import time
from itertools import chain
from typing import Dict, Optional, Union
import ssl

import redis

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
    def create(parameters: object, logger: object,
               direction: Optional[str] = None,
               queues: Optional[Union[str, list, dict]] = None,
               bot=None):
        """
        parameters: Parameters object
        direction: "source" or "destination", optional, needed for queues
        queues: needs direction to be set, calls set_queues
        bot: Bot instance
        """
        if direction not in [None, "source", "destination"]:
            raise exceptions.InvalidArgument("direction", got=direction,
                                             expected=["destination", "source"])
        if direction and hasattr(parameters, "%s_pipeline_broker" % direction):
            broker = getattr(parameters, "%s_pipeline_broker" % direction).title()
        elif (getattr(parameters, "source_pipeline_broker", None) == getattr(parameters, "destination_pipeline_broker", None) and
              getattr(parameters, "source_pipeline_broker", None) is not None):
            broker = getattr(parameters, "source_pipeline_broker").title()
        else:
            if hasattr(parameters, 'broker'):
                broker = parameters.broker.title()
            else:
                broker = "Redis"
        pipe = getattr(intelmq.lib.pipeline, broker)(parameters, logger, bot)
        if queues and not direction:
            raise ValueError("Parameter 'direction' must be given when using "
                             "the queues parameter.")
        elif queues:
            pipe.set_queues(queues, direction)

        return pipe


class Pipeline(object):
    has_internal_queues = False
    # If the class currently holds a message, restricts the actions
    _has_message = False

    def __init__(self, parameters, logger, bot):
        self.parameters = parameters
        self.destination_queues = {}  # type: dict[str, list]
        self.internal_queue = None
        self.source_queue = None
        self.logger = logger
        self.bot = bot

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def set_queues(self, queues: Optional[str], queues_type: str):
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

    def send(self, message: str, path: str = "_default",
             path_permissive: bool = False):
        raise NotImplementedError

    def receive(self) -> str:
        if self._has_message:
            raise exceptions.PipelineError("There's already a message, first "
                                           "acknowledge the existing one.")

        retval = self._receive()
        self._has_message = True
        return utils.decode(retval)

    def _receive(self) -> bytes:
        raise NotImplementedError

    def acknowledge(self):
        """
        Acknowledge/delete the current message from the source queue

        Parameters
        ----------

        Raises
        ------
        exceptions
            exceptions.PipelineError: If no message is held

        Returns
        -------
        None.

        """
        if not self._has_message:
            raise exceptions.PipelineError("No message to acknowledge.")
        self._acknowledge()
        self._has_message = False

    def _acknowledge(self):
        raise NotImplementedError

    def clear_queue(self, queue):
        raise NotImplementedError

    def nonempty_queues(self) -> set:
        raise NotImplementedError

    def reject_message(self):
        if not self._has_message:
            raise exceptions.PipelineError("No message to acknowledge.")
        self._reject_message()
        self._has_message = False

    def _reject_message(self):
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
        redis_version = tuple(int(x) for x in redis.__version__.split('.'))

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
        if self.bot and self.bot.is_multithreaded and redis_version >= (3, 3):
            # Should give a small performance increase, but is not thread-safe.
            kwargs['single_connection_client'] = True

        self.pipe = redis.Redis(db=self.db, password=self.password, **kwargs)

    def disconnect(self):
        pass

    def set_queues(self, queues, queues_type):
        self.load_configurations(queues_type)
        super().set_queues(queues, queues_type)

    def send(self, message: str, path: str = "_default",
             path_permissive: bool = False):
        if path not in self.destination_queues and path_permissive:
            return

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
                    raise IOError(28, 'No space left on device or in memory. Redis can\'t save its snapshots. '
                                      'Look at redis\'s logs.')
                raise exceptions.PipelineError(exc)

    def _receive(self) -> bytes:
        if self.source_queue is None:
            raise exceptions.ConfigurationError('pipeline', 'No source queue given.')
        try:
            while True:
                try:
                    retval = self.pipe.lindex(self.internal_queue, -1)  # returns None if no value
                except redis.exceptions.BusyLoadingError:  # Just wait at redis' startup #1334
                    time.sleep(1)
                else:
                    break
            if not retval:
                retval = self.pipe.brpoplpush(self.source_queue,
                                              self.internal_queue, 0)
        except Exception as exc:
            raise exceptions.PipelineError(exc)
        else:
            return retval

    def _acknowledge(self):
        try:
            retval = self.pipe.rpop(self.internal_queue)
        except Exception as exc:
            raise exceptions.PipelineError(exc)
        else:
            if not retval:
                raise exceptions.PipelineError("Could not pop message from internal queue "
                                               "for acknowledgement. Return value was %r."
                                               "" % retval)

    def count_queued_messages(self, *queues) -> dict:
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
            retval = self.pipe.delete(queue)
        except Exception as exc:
            raise exceptions.PipelineError(exc)
        else:
            if retval not in (0, 1):
                raise exceptions.PipelineError("Error on redis queue deletion: Return value"
                                               " was not 0 or 1 but %r." % retval)

    def nonempty_queues(self) -> set:
        """ Returns a list of all currently non-empty queues. """
        if not self.pipe:
            self.set_queues(None, "source")
            self.connect()
        return {queue.decode() for queue in self.pipe.keys()}

    def _reject_message(self):
        """
        Rejecting is a no-op as the message is in the internal queue anyway.
        """

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

    state = {}  # type: Dict[str, list]

    def connect(self):
        if self.parameters.raise_on_connect:
            raise exceptions.PipelineError('Connect failed as requested')

    def disconnect(self):
        pass

    def set_queues(self, queues, queues_type):
        super().set_queues(queues, queues_type)
        self.state[self.internal_queue] = []
        self.state[self.source_queue] = []
        for destination_queue in chain.from_iterable(self.destination_queues.values()):
            self.state[destination_queue] = []

    def send(self, message: str, path: str = "_default",
             path_permissive: bool = False):
        """Sends a message to the destination queues"""
        if path not in self.destination_queues and path_permissive:
            return

        for destination_queue in self.destination_queues[path]:
            if destination_queue in self.state:
                self.state[destination_queue].append(utils.encode(message))
            else:
                self.state[destination_queue] = [utils.encode(message)]

    def _receive(self) -> bytes:
        """
        Receives the last not yet acknowledged message.

        Does not block unlike the other pipelines.
        """
        if len(self.state[self.internal_queue]) > 0:
            return utils.decode(self.state[self.internal_queue][0])

        try:
            first_msg = self.state[self.source_queue].pop(0)
        except IndexError as exc:
            raise exceptions.PipelineError(exc)
        self.state[self.internal_queue].append(first_msg)

        return first_msg

    def _acknowledge(self):
        """Removes a message from the internal queue and returns it"""
        self.state.get(self.internal_queue, [None]).pop(0)

    def count_queued_messages(self, *queues) -> dict:
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

    def _reject_message(self):
        """
        No-op because of the internal queue
        """


class Amqp(Pipeline):
    queue_args = {'x-queue-mode': 'lazy'}

    def __init__(self, parameters, logger, bot):
        super(Amqp, self).__init__(parameters, logger, bot)
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
                                    "{}_pipeline_amqp_virtual_host".format(queues_type),
                                    '/')
        self.ssl = getattr(self.parameters,
                           "{}_pipeline_ssl".format(queues_type),
                           False)
        self.exchange = getattr(self.parameters,
                                "{}_pipeline_amqp_exchange".format(queues_type),
                                "")
        self.load_balance_iterator = 0
        self.kwargs = {}
        if self.username and self.password:
            self.kwargs['credentials'] = pika.PlainCredentials(self.username, self.password)
        if self.ssl:
            self.kwargs['ssl_options'] = pika.SSLOptions(context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))
        pika_version = tuple(int(x) for x in pika.__version__.split('.'))
        if pika_version < (0, 11):
            self.kwargs['heartbeat_interval'] = 10
        else:
            self.kwargs['heartbeat'] = 10
        if pika_version < (1, ):
            # https://groups.google.com/forum/#!topic/pika-python/gz7lZtPRq4Q
            self.publish_raises_nack = False
        else:
            self.publish_raises_nack = True

        self.monitoring_url = getattr(self.parameters,
                                      'intelmqctl_rabbitmq_monitoring_url',
                                      'http://%s:15672/' % self.host)
        if not self.monitoring_url.endswith('/'):
            self.monitoring_url = "%s/" % self.monitoring_url

    def connect(self):
        self.channel = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                            port=int(self.port),
                                                                            socket_timeout=self.socket_timeout,
                                                                            virtual_host=self.virtual_host,
                                                                            **self.kwargs
                                                                            ))
        self.setup_channel()

    def setup_channel(self):
        self.channel = self.connection.channel()
        self.channel.confirm_delivery()

        if self.exchange:
            # Do not declare and use queues if an exchange is given
            return
        if self.source_queue:
            self.channel.queue_declare(queue=self.source_queue, durable=True,
                                       arguments=self.queue_args)
        for path in self.destination_queues.values():
            for destination_queue in path:
                self.channel.queue_declare(queue=destination_queue, durable=True,
                                           arguments=self.queue_args)

    def check_connection(self):
        if not self.connection or self.connection.is_closed:
            self.connect()
        if not self.channel or self.channel.is_closed:
            self.setup_channel()

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

    def _send(self, destination_queue, message, reconnect=True):
        self.check_connection()

        retval = False
        try:
            retval = self.channel.basic_publish(exchange=self.exchange,
                                                routing_key=destination_queue,
                                                body=message,
                                                properties=self.properties,
                                                mandatory=True,
                                                )
        except Exception as exc:  # UnroutableError, NackError in 1.0.0
            if reconnect and isinstance(exc, pika.exceptions.ConnectionClosed):
                self.logger.debug('Error sending the message. '
                                  'Will re-connect and re-send.',
                                  exc_info=True)
                self.connect()
                self._send(destination_queue, message, reconnect=False)
            else:
                raise exceptions.PipelineError(exc)
        else:
            if not self.publish_raises_nack and not retval:
                raise exceptions.PipelineError('Sent message was not confirmed.')

    def send(self, message: str, path: str = "_default",
             path_permissive: bool = False):
        """
        In principle we could use AMQP's exchanges here but that architecture is incompatible
        to the format of our pipeline.conf file.
        """
        if path not in self.destination_queues and path_permissive:
            return

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

    def _receive(self) -> bytes:
        if self.source_queue is None:
            raise exceptions.ConfigurationError('pipeline', 'No source queue given.')
        try:
            method, header, body = next(self.channel.consume(self.source_queue))
            if method:
                self.delivery_tag = method.delivery_tag
        except Exception as exc:
            raise exceptions.PipelineError(exc)
        else:
            return body

    def _acknowledge(self):
        try:
            self.channel.basic_ack(delivery_tag=self.delivery_tag)
        except pika.exceptions.ConnectionClosed:
            self.logger.debug('Error sending the message. '
                              'Will re-connect and re-send.',
                              exc_info=True)
            self.connect()
            self.channel.basic_ack(delivery_tag=self.delivery_tag)
        except Exception as e:
            raise exceptions.PipelineError(e)
        else:
            self.delivery_tag = None

    def _get_queues(self) -> dict:
        if self.username and self.password:
            auth = (self.username, self.password)
        else:
            auth = ('guest', 'guest')
        if requests is None:
            self.logger.error("Library 'requests' is needed to get queue status. Please install it.")
            return {}
        response = requests.get(self.monitoring_url + 'api/queues', auth=auth,
                                timeout=5)
        if response.status_code == 401:
            if response.json()['error'] == 'not_authorised':
                # "Login failed", "Not management user"
                raise ValueError("User is not authorised: %r.", response.json()['reason'])
            else:
                raise ValueError("Unknown authentication failure: %r.", response.json())
        elif response.status_code != 200:
            raise ValueError("Unknown error %r.", response.text)
        try:
            return {x['name']: x.get('messages', 0) for x in response.json()}
        except SyntaxError:
            self.logger.error("Unable to parse response from server as JSON: %r.", response.text)
            return {}

    def count_queued_messages(self, *queues) -> dict:
        queue_dict = dict()
        response = self._get_queues()
        for queue in queues:
            queue_dict[queue] = response.get(queue, 0)
        return queue_dict

    def clear_queue(self, queue: str) -> bool:
        try:
            self.channel.queue_delete(queue=queue)
        except pika.exceptions.ChannelClosed:  # channel not found and similar
            pass

    def nonempty_queues(self) -> set:
        result = self._get_queues()
        return {name for name, count in result.items() if count}

    def _reject_message(self):
        self.channel.basic_nack(delivery_tag=self.delivery_tag, requeue=True)
