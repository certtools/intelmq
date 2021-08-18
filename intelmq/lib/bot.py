# SPDX-FileCopyrightText: 2014 Tomás Lima
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
The bot library has the base classes for all bots.
  * Bot: generic base class for all kind of bots
  * CollectorBot: base class for collectors
  * ParserBot: base class for parsers
  * SQLBot: base class for any bots using SQL
"""
import argparse
import atexit
import csv
import fcntl
import inspect
import io
import json
import logging
import os
import re
import signal
import sys
import threading
import time
import traceback
import types
import warnings
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, List, Optional, Union

import psutil

import intelmq.lib.message as libmessage
from intelmq import (DEFAULT_LOGGING_PATH,
                     HARMONIZATION_CONF_FILE,
                     RUNTIME_CONF_FILE, __version__)
from intelmq.lib import cache, exceptions, utils
from intelmq.lib.pipeline import PipelineFactory, Pipeline
from intelmq.lib.utils import RewindableFileHandle, base64_decode

__all__ = ['Bot', 'CollectorBot', 'ParserBot', 'SQLBot', 'OutputBot']


class Bot(object):
    """ Not to be reset when initialized again on reload. """
    __current_message: Optional[libmessage.Message] = None
    __message_counter_delay: timedelta = timedelta(seconds=2)
    __stats_cache: cache.Cache = None

    # Bot is capable of SIGHUP delaying
    _sighup_delay: bool = True
    # From the runtime configuration
    description: Optional[str] = None
    group: Optional[str] = None
    module = None
    name: Optional[str] = None
    # Imported from the legacy defaults.conf
    accuracy: int = 100
    destination_pipeline_broker: str = "redis"
    destination_pipeline_db: int = 2
    destination_pipeline_host: str = "127.0.0.1"
    destination_pipeline_password: Optional[str] = None
    destination_pipeline_port: int = 6379
    destination_queues: dict = {}
    error_dump_message: bool = True
    error_log_exception: bool = True
    error_log_message: bool = False
    error_max_retries: int = 3
    error_procedure: str = "pass"
    error_retry_delay: int = 15
    http_proxy: Optional[str] = None
    http_timeout_max_tries: int = 3
    http_timeout_sec: int = 30
    http_user_agent: str = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    http_verify_cert: Union[bool, str] = True
    https_proxy: Optional[str] = None
    instances_threads: int = 0
    load_balance: bool = False
    log_processed_messages_count: int = 500
    log_processed_messages_seconds: int = 900
    logging_handler: str = "file"
    logging_level: str = "INFO"
    logging_path: str = "/opt/intelmq/var/log/"
    logging_syslog: str = "/dev/log"
    process_manager: str = "intelmq"
    rate_limit: int = 0
    source_pipeline_broker: str = "redis"
    source_pipeline_db: int = 2
    source_pipeline_host: str = "127.0.0.1"
    source_pipeline_password: Optional[str] = None
    source_pipeline_port: int = 6379
    source_queue: Optional[str] = None
    ssl_ca_certificate: Optional[str] = None
    statistics_database: int = 3
    statistics_host: str = "127.0.0.1"
    statistics_password: Optional[str] = None
    statistics_port: int = 6379

    _message_processed_verb: str = 'Processed'

    # True for (non-main) threads of a bot instance
    is_multithreaded: bool = False
    # True if the bot is thread-safe and it makes sense
    __is_multithreadable: bool = True
    # Collectors with an empty process() should set this to true, prevents endless loops (#1364)
    __collector_empty_process: bool = False

    def __init__(self, bot_id: str, start: bool = False, sighup_event=None,
                 disable_multithreading: bool = None):

        self.__log_buffer: list = []

        self.__error_retries_counter: int = 0
        self.__source_pipeline: Optional[Pipeline] = None
        self.__destination_pipeline: Optional[Pipeline] = None
        self.logger = None

        self.__message_counter = {"since": 0,  # messages since last logging
                                  "start": None,  # last login time
                                  "success": 0,  # total number since the beginning
                                  "failure": 0,  # total number since the beginning
                                  "stats_timestamp": datetime.now(),  # stamp of last report to redis
                                  "path": defaultdict(int),  # number of messages sent to queues since last report to redis
                                  "path_total": defaultdict(int)  # number of messages sent to queues since beginning
                                  }

        try:
            version_info = sys.version.splitlines()[0].strip()
            self.__log_buffer.append(('info',
                                      '{bot} initialized with id {id} and intelmq {intelmq}'
                                      ' and python {python} as process {pid}.'
                                      ''.format(bot=self.__class__.__name__,
                                                id=bot_id, python=version_info,
                                                pid=os.getpid(), intelmq=__version__)))
            self.__log_buffer.append(('debug', 'Library path: %r.' % __file__))
            if not utils.drop_privileges():
                raise ValueError('IntelMQ must not run as root. Dropping privileges did not work.')

            self.__load_defaults_configuration()

            self.__bot_id_full, self.__bot_id, self.__instance_id = self.__check_bot_id(bot_id)
            if self.__instance_id:
                self.is_multithreaded = True
            self.__init_logger()
        except Exception:
            self.__log_buffer.append(('critical', traceback.format_exc()))
            self.stop()
        else:
            for line in self.__log_buffer:
                getattr(self.logger, line[0])(line[1])

        try:
            self.logger.info('Bot is starting.')
            self.__load_runtime_configuration()

            broker = self.source_pipeline_broker.title()
            if broker != 'Amqp':
                self.__is_multithreadable = False

            """ Multithreading """
            if (self.instances_threads > 1 and not self.is_multithreaded and
               self.__is_multithreadable and not disable_multithreading):
                self.logger.handlers = []
                num_instances = int(self.instances_threads)
                instances = []
                sighup_events = []

                def handle_sighup_signal_threading(signum: int,
                                                   stack: Optional[object]):
                    for event in sighup_events:
                        event.set()

                signal.signal(signal.SIGHUP, handle_sighup_signal_threading)

                for i in range(num_instances):
                    sighup_events.append(threading.Event())
                    threadname = '%s.%d' % (bot_id, i)
                    instances.append(threading.Thread(target=self.__class__,
                                                      kwargs={'bot_id': threadname,
                                                              'start': True,
                                                              'sighup_event': sighup_events[-1]},
                                                      name=threadname,
                                                      daemon=False))
                    instances[i].start()
                for i, thread in enumerate(instances):
                    thread.join()
                return
            elif (getattr(self, 'instances_threads', 1) > 1 and
                  not self.__is_multithreadable):
                self.logger.error('Multithreading is configured, but is not '
                                  'available for this bot. Look at the FAQ '
                                  'for a list of reasons for this. '
                                  'https://intelmq.readthedocs.io/en/latest/user/FAQ.html'
                                  '#multithreading-is-not-available-for-this-bot')
            elif (getattr(self, 'instances_threads', 1) > 1 and
                  disable_multithreading):
                self.logger.warning('Multithreading is configured, but is not '
                                    'available for interactive runs.')

            self.__load_harmonization_configuration()

            self._parse_common_parameters()

            super().__init__()
            self.__connect_pipelines()
            self.init()

            if not self.__instance_id:
                self.__sighup = threading.Event()
                signal.signal(signal.SIGHUP, self.__handle_sighup_signal)
                # system calls should not be interrupted, but restarted
                signal.siginterrupt(signal.SIGHUP, False)
                signal.signal(signal.SIGTERM, self.__handle_sigterm_signal)
                signal.signal(signal.SIGINT, self.__handle_sigterm_signal)
            else:
                self.__sighup = sighup_event

                @atexit.register
                def catch_shutdown():
                    self.stop()
        except Exception as exc:
            if self.error_log_exception:
                self.logger.exception('Bot initialization failed.')
            else:
                self.logger.error(utils.error_message_from_exc(exc))
                self.logger.error('Bot initialization failed.')

            self.stop()
            raise
        self.logger.info("Bot initialization completed.")

        self.__stats_cache = cache.Cache(host=self.statistics_host,
                                         port=self.statistics_port,
                                         db=int(self.statistics_database),
                                         password=self.statistics_password,
                                         ttl=None,
                                         )
        if start:
            self.start()

    def __handle_sigterm_signal(self, signum: int, stack: Optional[object]):
        """
        Calls when a SIGTERM is received. Stops the bot.
        """
        self.logger.info("Received SIGTERM.")
        self.stop(exitcode=0)

    def __handle_sighup_signal(self, signum: int, stack: Optional[object]):
        """
        Called when signal is received and postpone.
        """
        self.__sighup.set()
        if not self._sighup_delay:
            self.__handle_sighup()
        else:
            self.logger.info('Received SIGHUP, initializing again later.')

    def __handle_sighup(self):
        """
        Handle SIGHUP.
        """
        if not self.__sighup.is_set():
            return False
        self.logger.info('Handling SIGHUP, initializing again now.')
        self.__disconnect_pipelines()
        try:
            self.shutdown()  # disconnects, stops threads etc
        except Exception:
            self.logger.exception('Error during shutdown of bot.')
        self.logger.handlers = []  # remove all existing handlers
        self.__sighup.clear()
        self.__init__(self.__bot_id_full, sighup_event=self.__sighup)

    def init(self):
        pass

    def shutdown(self):
        pass

    def start(self, starting: bool = True, error_on_pipeline: bool = True,
              error_on_message: bool = False, source_pipeline: Optional[str] = None,
              destination_pipeline: Optional[str] = None):

        self.__source_pipeline = source_pipeline
        self.__destination_pipeline = destination_pipeline

        while True:
            try:
                if not starting and (error_on_pipeline or error_on_message):
                    self.logger.info('Bot will continue in %s seconds.',
                                     self.error_retry_delay)
                    time.sleep(self.error_retry_delay)

                starting: bool = False
                error_on_message: bool = False
                message_to_dump: Optional[dict] = None

                if error_on_pipeline:
                    try:
                        self.__connect_pipelines()
                    except Exception as exc:
                        raise exceptions.PipelineError(exc)
                    else:
                        error_on_pipeline = False

                self.__handle_sighup()
                self.process()
                self.__error_retries_counter = 0  # reset counter

            except exceptions.PipelineError as exc:
                error_on_pipeline = True

                if self.error_log_exception:
                    self.logger.exception('Pipeline failed.')
                else:
                    self.logger.error(utils.error_message_from_exc(exc))
                    self.logger.error('Pipeline failed.')
                self.__disconnect_pipelines()

            except exceptions.DecodingError as exc:
                self.logger.exception('Could not decode message from pipeline. No retries useful.')

                # ensure that we do not re-process the faulty message
                self.__error_retries_counter = self.error_max_retries + 1
                error_on_message = sys.exc_info()

                message_to_dump = exc.object

            except exceptions.InvalidValue as exc:
                self.logger.exception('Found an invalid value that violates the harmonization rules.')

                # ensure that we do not re-process the faulty message
                self.__error_retries_counter = self.error_max_retries + 1
                error_on_message = sys.exc_info()

                message_to_dump = exc.object

            except Exception as exc:
                # in case of serious system issues, exit immediately
                if isinstance(exc, MemoryError):
                    self.logger.exception('Out of memory. Exit immediately. Reason: %r.' % exc.args[0])
                    self.stop()
                elif isinstance(exc, (IOError, OSError)) and exc.errno == 28:
                    self.logger.exception('Out of disk space. Exit immediately.')
                    self.stop()

                error_on_message = sys.exc_info()

                if self.error_log_exception:
                    self.logger.exception("Bot has found a problem.")
                else:
                    self.logger.error(utils.error_message_from_exc(exc))
                    self.logger.error("Bot has found a problem.")

                if self.error_log_message:
                    # Print full message if explicitly requested by config
                    self.logger.info("Current Message(event): %r.",
                                     self.__current_message)

                # In case of permanent failures, stop now
                if isinstance(exc, exceptions.ConfigurationError):
                    self.stop()

            except KeyboardInterrupt:
                self.logger.info("Received KeyboardInterrupt.")
                self.stop(exitcode=0)

            finally:
                do_rate_limit: bool = False

                if error_on_message or error_on_pipeline:
                    self.__message_counter["failure"] += 1
                    self.__error_retries_counter += 1

                    # reached the maximum number of retries
                    if (self.__error_retries_counter >
                            self.error_max_retries):

                        if error_on_message:

                            if self.error_dump_message:
                                error_traceback = traceback.format_exception(*error_on_message)
                                self._dump_message(error_traceback,
                                                   message=message_to_dump if message_to_dump else self.__current_message)
                            else:
                                warnings.warn("Message will be removed from the pipeline and not dumped to the disk. "
                                              "Set `error_dump_message` to true to save the message on disk. "
                                              "This warning is only shown once in the runtime of a bot.")
                            if '_on_error' in self.destination_queues:
                                self.send_message(self.__current_message, path='_on_error')

                            if message_to_dump or self.__current_message:
                                self.acknowledge_message()

                            # when bot acknowledge the message,
                            # don't need to wait again
                            error_on_message = False

                        # run_mode: scheduled
                        if self.run_mode == 'scheduled':
                            self.logger.info('Shutting down scheduled bot.')
                            self.stop(exitcode=0)

                        # error_procedure: stop
                        elif self.error_procedure == "stop":
                            self.stop()

                        # error_procedure: pass
                        elif not error_on_pipeline:
                            self.__error_retries_counter = 0  # reset counter
                            do_rate_limit = True
                        # error_procedure: pass and pipeline problem
                        else:
                            # retry forever, see https://github.com/certtools/intelmq/issues/1333
                            # https://lists.cert.at/pipermail/intelmq-users/2018-October/000085.html
                            pass
                else:
                    self.__message_counter["success"] += 1
                    do_rate_limit = True

                    # no errors, check for run mode: scheduled
                    if self.run_mode == 'scheduled':
                        self.logger.info('Shutting down scheduled bot.')
                        self.stop(exitcode=0)

                if getattr(self, 'testing', False):
                    self.logger.debug('Testing environment detected, returning now.')
                    return

                # Do rate_limit at the end on success and after the retries
                # counter has been reset: https://github.com/certtools/intelmq/issues/1431
                if do_rate_limit:
                    if self.rate_limit and self.run_mode != 'scheduled':
                        self.__sleep()
                    if self.__collector_empty_process and self.run_mode != 'scheduled':
                        self.__sleep(1, log=False)

            self.__stats()
            self.__handle_sighup()

    def __stats(self, force: bool = False):
        """
        Flush stats to redis

        Only all self.__message_counter_delay (2 seconds), or with force=True
        """

        if not (force or datetime.now() - self.__message_counter["stats_timestamp"] > self.__message_counter_delay):
            return
        if not self.__stats_cache:
            # Cache not yet initialized, e.g. error in init
            return

        try:
            for path, n in self.__message_counter["path"].items():
                # current queue traffic
                self.__stats_cache.set(".".join((self.__bot_id_full, "temporary", path)), n, ttl=2)
                self.__message_counter["path_total"][path] += n
                self.__message_counter["path"][path] = 0
            for path, total in self.__message_counter["path_total"].items():
                # total queue traffic
                self.__stats_cache.set(".".join((self.__bot_id_full, "total", path)), total)
            self.__stats_cache.set(".".join((self.__bot_id_full, "stats", "success")),
                                   self.__message_counter["success"])
            self.__stats_cache.set(".".join((self.__bot_id_full, "stats", "failure")),
                                   self.__message_counter["failure"])
            self.__message_counter["stats_timestamp"] = datetime.now()
        except Exception:
            self.logger.debug('Failed to write statistics to cache, check your `statistics_*` settings.', exc_info=True)

    def __sleep(self, remaining: Optional[float] = None, log: bool = True):
        """
        Sleep handles interrupts and changed rate_limit-parameter.

        time.sleep is stopped by signals such as SIGHUP. As rate_limit could
        have been changed, we initialize again and continue to sleep, if
        necessary at all.

        Parameters:
            remaining: Time to sleep. 'rate_limit' parameter by default if None
            log: Log the remaining sleep time, default: True
        """
        starttime = time.time()
        if remaining is None:
            remaining = self.rate_limit

        while remaining > 0:
            if log:
                self.logger.info("Idling for {:.1f}s ({}) now.".format(remaining,
                                                                       utils.seconds_to_human(remaining)))
            time.sleep(remaining)
            self.__handle_sighup()
            remaining = self.rate_limit - (time.time() - starttime)

    def stop(self, exitcode: int = 1):
        if not self.logger:
            print('Could not initialize logger, only logging to stdout.')
        try:
            self.shutdown()
        except Exception:
            if self.logger:
                self.logger.exception('Error during shutdown of bot.')
            else:  # logger not yet initialized
                print('Error during shutdown of bot.')

        if self.__message_counter["since"]:
            if self.logger:
                self.logger.info("%s %d messages since last logging.",
                                 self._message_processed_verb,
                                 self.__message_counter["since"])
            else:
                print("%s %d messages since last logging." % (self._message_processed_verb,
                                                              self.__message_counter["since"]))

        self.__stats(force=True)
        self.__disconnect_pipelines()

        if self.logger:
            self.logger.info("Bot stopped.")
            logging.shutdown()
            # Bots using threads that do not exit properly, see #970
            if self.__class__.__name__ in ['XMPPCollectorBot', 'XMPPOutputBot']:
                proc = psutil.Process(os.getpid())
                proc.send_signal(signal.SIGTERM)
        else:
            self.__log_buffer.append(('info', 'Bot stopped.'))
            self.__print_log_buffer()

        if not getattr(self, 'testing', False):
            sys.exit(exitcode)

    def __print_log_buffer(self):
        for level, message in self.__log_buffer:
            if self.logger:
                getattr(self.logger, level)(message)
            if level in ['WARNING', 'ERROR', 'critical']:
                print(level.upper(), '-', message, file=sys.stderr)
            else:
                print(level.upper(), '-', message)
        self.__log_buffer = []

    def __check_bot_id(self, name: str):
        res = re.fullmatch(r'([0-9a-zA-Z\-]+)(\.[0-9]+)?', name)
        if res:
            if not (res.group(2) and threading.current_thread() == threading.main_thread()):
                return name, res.group(1), res.group(2)[1:] if res.group(2) else None
        self.__log_buffer.append(('error',
                                  "Invalid bot id, must match '"
                                  r"[^0-9a-zA-Z\-]+'."))
        self.stop()

    def __connect_pipelines(self):
        pipeline_args = {key: getattr(self, key) for key in dir(self) if not inspect.ismethod(getattr(self, key)) and (key.startswith('source_pipeline_') or key.startswith('destination_pipeline'))}
        if self.source_queue is not None:
            self.logger.debug("Loading source pipeline and queue %r.", self.source_queue)
            self.__source_pipeline = PipelineFactory.create(logger=self.logger,
                                                            direction="source",
                                                            queues=self.source_queue,
                                                            pipeline_args=pipeline_args,
                                                            load_balance=self.load_balance,
                                                            is_multithreaded=self.is_multithreaded)

            self.__source_pipeline.connect()
            self.__current_message = None
            self.logger.debug("Connected to source queue.")

        if self.destination_queues:
            self.logger.debug("Loading destination pipeline and queues %r.", self.destination_queues)
            self.__destination_pipeline = PipelineFactory.create(logger=self.logger,
                                                                 direction="destination",
                                                                 queues=self.destination_queues,
                                                                 pipeline_args=pipeline_args,
                                                                 load_balance=self.load_balance,
                                                                 is_multithreaded=self.is_multithreaded)

            self.__destination_pipeline.connect()
            self.logger.debug("Connected to destination queues.")
        else:
            self.logger.debug("No destination queues to load.")

    def __disconnect_pipelines(self):
        """ Disconnecting pipelines. """
        if self.__source_pipeline:
            self.__source_pipeline.disconnect()
            self.__source_pipeline = None
            self.logger.debug("Disconnected from source pipeline.")
        if self.__destination_pipeline:
            self.__destination_pipeline.disconnect()
            self.__destination_pipeline = None
            self.logger.debug("Disconnected from destination pipeline.")

    def send_message(self, *messages, path: str = "_default", auto_add=None,
                     path_permissive: bool = False):
        """
        Parameters:
            messages: Instances of intelmq.lib.message.Message class
            auto_add: ignored
            path_permissive: If true, do not raise an error if the path is
                not configured
        """
        for message in messages:
            if not message:
                self.logger.warning("Ignoring empty message at sending. Possible bug in bot.")
                continue
            if not self.__destination_pipeline:
                raise exceptions.ConfigurationError('pipeline', 'No destination pipeline given, '
                                                                'but needed')

            self.logger.debug("Sending message to path %r.", path)
            self.__message_counter["since"] += 1
            self.__message_counter["path"][path] += 1
            if not self.__message_counter["start"]:
                self.__message_counter["start"] = datetime.now()
            if self.__message_counter["since"] % self.log_processed_messages_count == 0 or \
                    datetime.now() - self.__message_counter["start"] > self.__log_processed_messages_seconds:
                self.logger.info("%s %d messages since last logging.",
                                 self._message_processed_verb,
                                 self.__message_counter["since"])
                self.__message_counter["since"] = 0
                self.__message_counter["start"] = datetime.now()

            raw_message = libmessage.MessageFactory.serialize(message)
            self.__destination_pipeline.send(raw_message, path=path,
                                             path_permissive=path_permissive)

    def receive_message(self) -> libmessage.Message:
        """


        If the bot is reloaded when waiting for an incoming message, the received message
        will be rejected to the pipeline in the first place to get to a clean state.
        Then, after reloading, the message will be retrieved again.
        """
        if self.__current_message:
            self.logger.debug("Reusing existing current message as incoming.")
            return self.__current_message

        self.logger.debug('Waiting for incoming message.')
        message = None
        while not message:
            message = self.__source_pipeline.receive()
            if not message:
                self.logger.warning('Empty message received. Some previous bot sent invalid data.')
                self.__handle_sighup()
                continue

        # * handle a sighup which happened during blocking read
        # * re-queue the message before reloading
        #   https://github.com/certtools/intelmq/issues/1438
        if self.__sighup.is_set():
            self.__source_pipeline.reject_message()
            self.__handle_sighup()
            return self.receive_message()

        try:
            self.__current_message = libmessage.MessageFactory.unserialize(message,
                                                                           harmonization=self.harmonization)
        except exceptions.InvalidKey as exc:
            # In case a incoming message is malformed an does not conform with the currently
            # loaded harmonization, stop now as this will happen repeatedly without any change
            raise exceptions.ConfigurationError('harmonization', exc.args[0])

        if self.logger.isEnabledFor(logging.DEBUG):
            if 'raw' in self.__current_message and len(self.__current_message['raw']) > 400:
                tmp_msg = self.__current_message.to_dict(hierarchical=False)
                tmp_msg['raw'] = tmp_msg['raw'][:397] + '...'
            else:
                tmp_msg = self.__current_message
            self.logger.debug('Received message %r.', tmp_msg)

        return self.__current_message

    def acknowledge_message(self):
        """
        Acknowledges that the last message has been processed, if any.

        For bots without source pipeline (collectors), this is a no-op.
        """
        if self.__source_pipeline:
            self.__source_pipeline.acknowledge()

        # free memory of last message
        self.__current_message = None

    def _dump_message(self, error_traceback, message: dict):
        if message is None or getattr(self, 'testing', False):
            return

        self.logger.info('Dumping message to dump file.')

        dump_file = os.path.join(self.logging_path, self.__bot_id + ".dump")

        timestamp = datetime.utcnow()
        timestamp: str = timestamp.isoformat()
        new_dump_data: dict = {}
        new_dump_data[timestamp]: dict = {}
        new_dump_data[timestamp]["bot_id"] = self.__bot_id
        new_dump_data[timestamp]["source_queue"] = self.source_queue
        new_dump_data[timestamp]["traceback"] = error_traceback

        if isinstance(message, bytes):
            # decoding errors
            new_dump_data[timestamp]["message"] = utils.base64_encode(message)
            new_dump_data[timestamp]["message_type"] = 'base64'
        else:
            new_dump_data[timestamp]["message"] = message.serialize()

        if os.path.exists(dump_file):
            # existing dump
            mode = 'r+'
        else:
            # new dump file
            mode = 'w'
        with open(dump_file, mode) as fp:
            for i in range(60):
                try:
                    fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    if i == 0:
                        self.logger.warning('Dump file is locked, waiting up to 60s.')
                    time.sleep(1)
                else:
                    break
            else:
                raise ValueError('Dump file was locked for more than 60s, giving up now.')
            if mode == 'r+':
                dump_data = json.load(fp)
                dump_data.update(new_dump_data)
            else:
                dump_data = new_dump_data

            fp.seek(0)

            json.dump(dump_data, fp, indent=4, sort_keys=True)

        self.logger.debug('Message dumped.')

    def __load_defaults_configuration(self):
        config = utils.get_global_settings()

        setattr(self, 'logging_path', DEFAULT_LOGGING_PATH)

        for option, value in config.items():
            setattr(self, option, value)
            self.__log_configuration_parameter("defaults", option, value)

        self.__log_processed_messages_seconds = timedelta(seconds=self.log_processed_messages_seconds)

    def __load_runtime_configuration(self):
        self.logger.debug("Loading runtime configuration from %r.", RUNTIME_CONF_FILE)
        config = utils.load_configuration(RUNTIME_CONF_FILE)
        reinitialize_logging = False

        if self.__bot_id in config:
            params = config[self.__bot_id]
            self.run_mode = params.get('run_mode', 'continuous')
            self.name = params.get('name')
            self.description = params.get('description')
            self.group = params.get('group')
            self.module = params.get('module')
            for option, value in params.get('parameters', {}).items():
                setattr(self, option, value)
                self.__log_configuration_parameter("runtime", option, value)
                if option.startswith('logging_'):
                    reinitialize_logging = True

        intelmq_environment = [elem for elem in os.environ if elem.startswith('INTELMQ_')]
        for elem in intelmq_environment:
            option = elem[8:].lower()
            value = os.environ[elem]
            # do some conversions:
            if value == 'True':
                value = True
            elif value == 'False':
                value = False
            elif value.isnumeric():
                value = int(value)

            setattr(self, option, value)
            self.__log_configuration_parameter("environment", option, value)

        if reinitialize_logging:
            self.logger.handlers = []  # remove all existing handlers
            self.__init_logger()

        # The default source_queue should be "{bot-id}-queue",
        # but this can be overridden
        if self.source_queue is None:
            self.source_queue = f"{self.__bot_id}-queue"

    def __init_logger(self):
        """
        Initialize the logger.
        """
        if self.logging_handler == 'syslog':
            syslog = self.logging_syslog
        else:
            syslog = False
        self.logger = utils.log(self.__bot_id_full, syslog=syslog,
                                log_path=self.logging_path,
                                log_level=self.logging_level,
                                log_max_size=getattr(self, "logging_max_size", 0),
                                log_max_copies=getattr(self, "logging_max_copies", None))

    def __log_configuration_parameter(self, config_name: str, option: str, value: Any):
        if "password" in option or "token" in option:
            value = "HIDDEN"

        message = "{} configuration: parameter {!r} loaded with value {!r}." \
            .format(config_name.title(), option, value)

        if self.logger:
            self.logger.debug(message)
        else:
            self.__log_buffer.append(("debug", message))

    def __load_harmonization_configuration(self):
        self.logger.debug("Loading Harmonization configuration from %r.", HARMONIZATION_CONF_FILE)
        self.harmonization = utils.load_configuration(HARMONIZATION_CONF_FILE)

    def new_event(self, *args, **kwargs):
        return libmessage.Event(*args, harmonization=self.harmonization, **kwargs)

    @classmethod
    def run(cls, parsed_args=None):

        if not parsed_args:
            parsed_args = cls._create_argparser().parse_args()

        if not parsed_args.bot_id:
            sys.exit('No bot ID given.')

        instance = cls(parsed_args.bot_id)
        if not instance.is_multithreaded:
            instance.start()

    def set_request_parameters(self):
        self.http_header: dict = getattr(self, 'http_header', {})
        self.http_verify_cert: bool = getattr(self, 'http_verify_cert', True)
        self.ssl_client_cert: Optional[str] = getattr(self, 'ssl_client_certificate', None)

        if (hasattr(self, 'http_username') and
                hasattr(self, 'http_password') and
                self.http_username):
            self.auth = (self.http_username,
                         self.http_password)
        else:
            self.auth = None

        if self.http_proxy and self.https_proxy:
            self.proxy = {'http': self.http_proxy,
                          'https': self.https_proxy}
        elif self.http_proxy or self.https_proxy:
            self.logger.warning('Only %s_proxy seems to be set.'
                                'Both http and https proxies must be set.',
                                'http' if self.http_proxy else 'https')
            self.proxy = {}
        else:
            self.proxy = {}

        self.http_timeout_sec: Optional[int] = getattr(self, 'http_timeout_sec', None)
        self.http_timeout_max_tries: int = getattr(self, 'http_timeout_max_tries', 1)
        # Be sure this is always at least 1
        self.http_timeout_max_tries = self.http_timeout_max_tries if self.http_timeout_max_tries >= 1 else 1

        self.http_header['User-agent'] = self.http_user_agent

    @staticmethod
    def check(parameters: dict) -> Optional[List[List[str]]]:
        """
        The bot's own check function can perform individual checks on it's
        parameters.
        `init()` is *not* called before, this is a staticmethod which does not
        require class initialization.

        Parameters:
            parameters: Bot's parameters, defaults and runtime merged together

        Returns:
            output: None or a list of [log_level, log_message] pairs, both
                strings. log_level must be a valid log level.
        """
        pass

    def _parse_common_parameters(self):
        """
        Parses and sanitizes commonly used parameters:

         * extract_files
        """
        self._parse_extract_file_parameter('extract_files')

    def _parse_extract_file_parameter(self, parameter_name: str = 'extract_files'):
        """
        Parses and sanitizes commonly used parameters:

         * extract_files
        """
        parameter_value = getattr(self, parameter_name, None)
        setattr(self, parameter_name, parameter_value)
        if parameter_value and isinstance(parameter_value, str):
            setattr(self, parameter_name, parameter_value.split(","))
            self.logger.debug('Extracting files from archives: '
                              "'%s'.", "', '".join(getattr(self, parameter_name)))
        elif parameter_value and isinstance(parameter_value, (list, tuple)):
            self.logger.debug('Extracting files from archives: '
                              "'%s'.", "', '".join(parameter_value))
        elif parameter_value:
            self.logger.debug('Extracting all files from archives.')

    @classmethod
    def _create_argparser(cls):
        """
        see https://github.com/certtools/intelmq/pull/1524/files#r464606370
        why this code is not in the constructor
        """
        argparser = argparse.ArgumentParser(usage='%(prog)s [OPTIONS] BOT-ID')
        argparser.add_argument('bot_id', nargs='?', metavar='BOT-ID', help='unique bot-id of your choosing')
        return argparser


class ParserBot(Bot):
    _csv_params = {}
    _ignore_lines_starting = []
    _handle = None
    _current_line = None

    def __init__(self, bot_id: str, start: bool = False, sighup_event=None,
                 disable_multithreading: bool = None):
        super().__init__(bot_id=bot_id)
        if self.__class__.__name__ == 'ParserBot':
            self.logger.error('ParserBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()
        self.group = 'Parser'

    def parse_csv(self, report: libmessage.Report):
        """
        A basic CSV parser.
        """
        raw_report: str = utils.base64_decode(report.get("raw")).strip()
        raw_report = raw_report.translate({0: None})
        if self._ignore_lines_starting:
            raw_report = '\n'.join([line for line in raw_report.splitlines()
                                    if not any([line.startswith(prefix) for prefix
                                                in self._ignore_lines_starting])])
        self._handle = RewindableFileHandle(io.StringIO(raw_report))
        for line in csv.reader(self._handle, **self._csv_params):
            self._current_line = self._handle.current_line
            yield line

    def parse_csv_dict(self, report: libmessage.Report):
        """
        A basic CSV Dictionary parser.
        """
        raw_report: str = utils.base64_decode(report.get("raw")).strip()
        raw_report: str = raw_report.translate({0: None})
        if self._ignore_lines_starting:
            raw_report = '\n'.join([line for line in raw_report.splitlines()
                                    if not any([line.startswith(prefix) for prefix
                                                in self._ignore_lines_starting])])
        self._handle = RewindableFileHandle(io.StringIO(raw_report))

        csv_reader = csv.DictReader(self._handle, **self._csv_params)
        # create an array of fieldnames,
        # those were automagically created by the dictreader
        self.csv_fieldnames = csv_reader.fieldnames

        for line in csv_reader:
            self._current_line = self._handle.current_line
            yield line

    def parse_json(self, report: libmessage.Report):
        """
        A basic JSON parser. Assumes a *list* of objects as input to be yield.
        """
        raw_report: str = utils.base64_decode(report.get("raw"))
        for line in json.loads(raw_report):
            yield line

    def parse_json_stream(self, report: libmessage.Report):
        """
        A JSON Stream parses (one JSON data structure per line)
        """
        raw_report: str = utils.base64_decode(report.get("raw"))
        for line in raw_report.splitlines():
            self._current_line = line
            yield json.loads(line)

    def parse(self, report: libmessage.Report):
        """
        A generator yielding the single elements of the data.

        Comments, headers etc. can be processed here. Data needed by
        `self.parse_line` can be saved in `self.tempdata` (list).

        Default parser yields stripped lines.
        Override for your use or use an existing parser, e.g.::

            parse = ParserBot.parse_csv

        You should do that for recovering lines too.
            recover_line = ParserBot.recover_line_csv

        """
        for line in utils.base64_decode(report.get("raw")).splitlines():
            line = line.strip()
            if not any([line.startswith(prefix) for prefix in self._ignore_lines_starting]):
                yield line

    def parse_line(self, line: Any, report: libmessage.Report):
        """
        A generator which can yield one or more messages contained in line.

        Report has the full message, thus you can access some metadata.
        Override for your use.
        """
        raise NotImplementedError

    def process(self):
        self.tempdata: list = []  # temporary data for parse, parse_line and recover_line
        self.__failed: list = []
        report: libmessage.Report = self.receive_message()

        if 'raw' not in report:
            self.logger.warning('Report without raw field received. Possible '
                                'bug or misconfiguration in previous bots.')
            self.acknowledge_message()
            return

        events_count: int = 0

        for line in self.parse(report):

            if not line:
                continue
            try:
                value = self.parse_line(line, report)
                if value is None:
                    continue
                elif type(value) is list or isinstance(value, types.GeneratorType):
                    # filter out None
                    events: list[libmessage.Event] = list(filter(bool, value))
                else:
                    events: list[libmessage.Event] = [value]
            except Exception:
                self.logger.exception('Failed to parse line.')
                self.__failed.append((traceback.format_exc(), line))
            else:
                events_count += len(events)
                self.send_message(*events)

        for exc, line in self.__failed:
            report_dump: libmessage.Message = report.copy()
            report_dump.change('raw', self.recover_line(line))
            if self.error_dump_message:
                self._dump_message(exc, report_dump)
            if self.destination_queues and '_on_error' in self.destination_queues:
                self.send_message(report_dump, path='_on_error')

        self.logger.info('Sent %d events and found %d problem(s).', events_count, len(self.__failed))

        self.acknowledge_message()

    def recover_line(self, line: Optional[str] = None) -> str:
        """
        Reverse of "parse" for single lines.

        Recovers a fully functional report with only the problematic line by
        concatenating all strings in "self.tempdata" with "line" with LF
        newlines. Works fine for most text files.

        Parameters
        ----------
        line : Optional[str], optional
            The currently process line which should be transferred into it's
            original appearance. As fallback, "self._current_line" is used if
            available (depending on self.parse).
            The default is None.

        Raises
        ------
        ValueError
            If neither the parameter "line" nor the member "self._current_line"
            is available.

        Returns
        -------
        str
            The reconstructed raw data.

        """
        if self._handle and self._handle.first_line and not self.tempdata:
            tempdata = [self._handle.first_line.strip()]
        else:
            tempdata = self.tempdata
        if not line and not self._current_line:
            raise ValueError('Parameter "line" is not given and '
                             '"self._current_line" is also None. Please give one of them.')
        line = line if line else self._current_line
        return '\n'.join(tempdata + [line])

    def recover_line_csv(self, line: str) -> str:
        out = io.StringIO()
        writer = csv.writer(out, **self._csv_params)
        writer.writerow(line)
        tempdata = '\r\n'.join(self.tempdata) + '\r\n' if self.tempdata else ''
        return tempdata + out.getvalue()

    def recover_line_csv_dict(self, line: str) -> str:
        """
        Converts dictionaries to csv. self.csv_fieldnames must be list of fields.
        """
        out = io.StringIO()
        writer = csv.DictWriter(out, self.csv_fieldnames, **self._csv_params)
        writer.writeheader()
        out.write(self._current_line)

        return out.getvalue().strip()

    def recover_line_json(self, line: dict) -> str:
        """
        Reverse of parse for JSON pulses.

        Recovers a fully functional report with only the problematic pulse.
        """
        return json.dumps([line])

    def recover_line_json_stream(self, line=None) -> str:
        """
        recover_line for json streams, just returns the current line, unparsed.

        Parameters
        ----------
        line : None, not required, only for compatibility with other recover_line methods

        Returns
        -------
        str
            unparsed JSON line.
        """
        return self._current_line


class CollectorBot(Bot):
    """
    Base class for collectors.

    Does some sanity checks on message sending.
    """

    __is_multithreadable: bool = False
    name: Optional[str] = None
    accuracy: int = 100
    code: Optional[str] = None
    provider: Optional[str] = None
    documentation: Optional[str] = None

    def __init__(self, bot_id: str, start: bool = False, sighup_event=None,
                 disable_multithreading: bool = None):
        super().__init__(bot_id=bot_id)
        if self.__class__.__name__ == 'CollectorBot':
            self.logger.error('CollectorBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()
        self.group = 'Collector'

    def __filter_empty_report(self, message: libmessage.Report):
        if 'raw' not in message:
            self.logger.warning('Ignoring report without raw field. '
                                'Possible bug or misconfiguration of this bot.')
            return False
        return True

    def __add_report_fields(self, report: libmessage.Report):
        """
        Adds the configured feed parameters to the report, of they are set (!= None).
        The following parameters are set to these report fields:
            * name -> feed.name
            * code -> feed.code
            * documentation -> feed.documentation
            * provider -> feed.provider
            * accuracy -> feed.accuracy
        """
        if self.name:
            report.add("feed.name", self.name)
        if self.code:
            report.add("feed.code", self.code)
        if self.documentation:
            report.add("feed.documentation", self.documentation)
        if self.provider:
            report.add("feed.provider", self.provider)
        if self.accuracy:
            report.add("feed.accuracy", self.accuracy)
        return report

    def send_message(self, *messages, path: str = "_default", auto_add: bool = True):
        """"
        Parameters:
            messages: Instances of intelmq.lib.message.Message class
            path: Named queue the message will be send to
            auto_add: Add some default report fields form parameters
        """
        messages = filter(self.__filter_empty_report, messages)
        if auto_add:
            messages = map(self.__add_report_fields, messages)
        super().send_message(*messages, path=path)

    def new_report(self):
        return libmessage.Report()


class SQLBot(Bot):
    """
    Inherit this bot so that it handles DB connection for you.
    You do not have to bother:
        * connecting database in the self.init() method, just call super().init(), self.cur will be set
        * catching exceptions, just call self.execute() instead of self.cur.execute()
        * self.format_char will be set to '%s' in PostgreSQL and to '?' in SQLite
    """

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    default_engine = "postgresql"

    def init(self):
        self.engine_name = getattr(self, 'engine', self.default_engine).lower()
        engines = {SQLBot.POSTGRESQL: (self._init_postgresql, "%s"),
                   SQLBot.SQLITE: (self._init_sqlite, "?")}
        for key, val in engines.items():
            if self.engine_name == key:
                val[0]()
                self.format_char = val[1]
                break
        else:
            raise ValueError("Wrong parameter 'engine' {0!r}, possible values are {1}".format(self.engine_name, engines))

    def _connect(self, engine, connect_args: dict, autocommitable: bool = False):
        self.engine = engine  # imported external library that connects to the DB
        self.logger.debug("Connecting to database.")

        try:
            self.con = self.engine.connect(**connect_args)
            if autocommitable:  # psycopg2 has it, sqlite3 has not
                self.con.autocommit = getattr(self, 'autocommit', True)  # True prevents deadlocks
            self.cur = self.con.cursor()
        except (self.engine.Error, Exception):
            self.logger.exception('Failed to connect to database.')
            self.stop()
        self.logger.info("Connected to database.")

    def _init_postgresql(self):
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError:
            raise exceptions.MissingDependencyError("psycopg2")

        self._connect(psycopg2,
                      {"database": self.database,
                       "user": self.user,
                       "password": self.password,
                       "host": self.host,
                       "port": self.port,
                       "sslmode": self.sslmode,
                       "connect_timeout": getattr(self, 'connect_timeout', 5)
                       },
                      autocommitable=True)

    def _init_sqlite(self):
        try:
            import sqlite3
        except ImportError:
            raise exceptions.MissingDependencyError("sqlite3")

        self._connect(sqlite3,
                      {"database": self.database,
                       "timeout": getattr(self, 'connect_timeout', 5)
                       }
                      )

    def execute(self, query: str, values: tuple, rollback=False):
        try:
            self.logger.debug('Executing %r.', (query, values))
            # note: this assumes, the DB was created with UTF-8 support!
            self.cur.execute(query, values)
            self.logger.debug('Done.')
        except (self.engine.InterfaceError, self.engine.InternalError,
                self.engine.OperationalError, AttributeError):
            if rollback:
                try:
                    self.con.rollback()
                    self.logger.exception('Executed rollback command '
                                          'after failed query execution.')
                except self.engine.OperationalError:
                    self.logger.exception('Executed rollback command '
                                          'after failed query execution.')
                    self.init()
                except Exception:
                    self.logger.exception('Cursor has been closed, connecting '
                                          'again.')
                    self.init()
            else:
                self.logger.exception('Database connection problem, connecting again.')
                self.init()
        else:
            return True
        return False


class OutputBot(Bot):
    """
    Base class for outputs.
    """

    def __init__(self, bot_id: str, start: bool = False, sighup_event=None,
                 disable_multithreading: bool = None):
        super().__init__(bot_id=bot_id)
        if self.__class__.__name__ == 'OutputBot':
            self.logger.error('OutputBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()
        self.group = 'Output'

        self.hierarchical: bool = getattr(self, "hierarchical_output",  # file and files
                                          getattr(self, "message_hierarchical",  # stomp and amqp code
                                                  getattr(self, "message_hierarchical_output", False)))  # stomp and amqp docs
        self.with_type: bool = getattr(self, "message_with_type", False)
        self.jsondict_as_string: bool = getattr(self, "message_jsondict_as_string", False)

        self.single_key: Optional[str] = getattr(self, 'single_key', None)
        self.keep_raw_field: bool = getattr(self, 'keep_raw_field', False)

    def export_event(self, event: libmessage.Event,
                     return_type: Optional[type] = None) -> Union[str, dict]:
        """
        exports an event according to the following parameters:
            * message_hierarchical
            * message_with_type
            * message_jsondict_as_string
            * single_key
            * keep_raw_field

        Parameters:
            return_type: Ensure that the returned value is of the given type.
                Optional. For example: str
                If the resulting value is not an instance of this type, the
                given object is called with the value as parameter E.g. `str(retval)`
        """
        if self.single_key:
            if self.single_key == 'raw':
                return base64_decode(event.get('raw', ''))
            elif self.single_key == 'output':
                retval = event.get(self.single_key)
                if return_type is str:
                    loaded = json.loads(retval)
                    if isinstance(loaded, return_type):
                        return loaded
                else:
                    retval = json.loads(retval)
            else:
                retval = event.get(self.single_key)
        else:
            if not self.keep_raw_field:
                if 'raw' in event:
                    del event['raw']
            if return_type is str:
                return event.to_json(hierarchical=self.hierarchical,
                                     with_type=self.with_type,
                                     jsondict_as_string=self.jsondict_as_string)
            else:
                retval = event.to_dict(hierarchical=self.hierarchical,
                                       with_type=self.with_type,
                                       jsondict_as_string=self.jsondict_as_string)

        if return_type and not isinstance(retval, return_type):
            return return_type(retval)
        return retval


class Parameters(object):
    pass
