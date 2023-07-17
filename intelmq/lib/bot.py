# SPDX-FileCopyrightText: 2014 Tomás Lima
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
The bot library has the base classes for all bots.
  * Bot: generic base class for all kind of bots
  * CollectorBot: base class for collectors
  * ParserBot: base class for parsers
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
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, List, Optional, Union, Tuple
from pkg_resources import resource_filename

import intelmq.lib.message as libmessage
from intelmq import (DEFAULT_LOGGING_PATH,
                     DEFAULT_LOGGING_LEVEL,
                     HARMONIZATION_CONF_FILE,
                     RUNTIME_CONF_FILE, __version__)
from intelmq.lib import cache, exceptions, utils
from intelmq.lib.pipeline import PipelineFactory, Pipeline
from intelmq.lib.utils import RewindableFileHandle, base64_decode
from intelmq.lib.datatypes import BotType, Dict39

__all__ = ['Bot', 'CollectorBot', 'ParserBot', 'OutputBot', 'ExpertBot']
ALLOWED_SYSTEM_PARAMETERS = {'enabled', 'run_mode', 'group', 'description', 'module', 'name'}
# The first two keys are only used by the IntelMQ Manager and can be ignored, the last just contains the runtime parameters and is handled separately
IGNORED_SYSTEM_PARAMETERS = {'groupname', 'bot_id', 'parameters'}


class Bot:
    """ Not to be reset when initialized again on reload. """
    __current_message: Optional[libmessage.Message] = None
    __message_counter: dict = {"since": None}
    __message_counter_delay: timedelta = timedelta(seconds=2)
    __stats_cache: cache.Cache = None
    __source_pipeline = None
    __destination_pipeline = None
    __log_buffer: List[tuple] = []
    # runtime_file
    __runtime_settings: Optional[dict] = None
    # settings provided via parameter
    __settings: Optional[dict] = None
    # if messages should be serialized/unserialized coming from/sending to the pipeline
    __pipeline_serialize_messages = True
    # if the Bot is running by itself or called by other procedures
    _standalone: bool = False

    logger = None
    # Bot is capable of SIGHUP delaying
    _sighup_delay: bool = True
    # From the runtime configuration
    enabled: bool = True
    run_mode: str = "continuous"
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
    logging_level: str = DEFAULT_LOGGING_LEVEL
    logging_path: str = DEFAULT_LOGGING_PATH
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
    _is_multithreadable: bool = True
    # Collectors with an empty process() should set this to true, prevents endless loops (#1364)
    _collector_empty_process: bool = False

    _harmonization: dict = {}

    def __init__(self, bot_id: str, start: bool = False, sighup_event=None,
                 disable_multithreading: bool = None, settings: Optional[dict] = None,
                 source_queue: Optional[str] = None, standalone: bool = False):

        self.__log_buffer: list = []

        self.__error_retries_counter: int = 0
        self.__source_pipeline: Optional[Pipeline] = None
        self.__destination_pipeline: Optional[Pipeline] = None
        self.logger = None
        if settings is not None:
            # make a copy of the settings dict, to no modify the original values of the caller
            self.__settings = deepcopy(settings)
        if source_queue is not None:
            self.source_queue = source_queue
        self._standalone = standalone

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
            self.__log('info',
                       f'{self.__class__.__name__} initialized with id {bot_id} and intelmq {__version__}'
                       f' and python {version_info} as process {os.getpid()}.')
            self.__log('debug', f'Library path: {__file__!r}.')

            # in standalone mode, drop privileges
            # In library mode, the calling user can vary, we must not change their user
            if self._standalone and not utils.drop_privileges():
                raise ValueError('IntelMQ must not run as root. Dropping privileges did not work.')

            self.__bot_id_full, self.__bot_id, self.__instance_id = self.__check_bot_id(bot_id)

            self.__load_configuration()

            if self.__instance_id:
                self.is_multithreaded = True
            self.__init_logger()
        except Exception:
            self.__log('critical', traceback.format_exc())
            self.stop()
        else:
            for line in self.__log_buffer:
                getattr(self.logger, line[0])(line[1])

        try:
            self.logger.info('Bot is starting.')

            broker = self.source_pipeline_broker.title()
            if broker != 'Amqp':
                self._is_multithreadable = False
                # multithreading is not (yet) available in library-mode
            elif not self._standalone:
                self._is_multithreadable = False

            """ Multithreading """
            if (self.instances_threads > 1 and not self.is_multithreaded and
               self._is_multithreadable and not disable_multithreading):
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
                  not self._is_multithreadable):
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
            self.__reset_total_path_stats()
            self.init()

            # only the main thread registers the signal handlers
            # in library-mode, handle no signals to not interfere with the caller
            if not self.__instance_id and self._standalone:
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
                    self.stop(exitcode=0)
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

    @property
    def harmonization(self):
        return self._harmonization

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
        if not self.__sighup or not self.__sighup.is_set():
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
                    if self._collector_empty_process and self.run_mode != 'scheduled':
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

    def __reset_total_path_stats(self):
        """Initially set destination paths to 0 to reset them in stats cache"""
        if not self.destination_queues:
            return
        queues_type = type(self.destination_queues)
        if queues_type is dict:
            for path in self.destination_queues.keys():
                self.__message_counter["path_total"][path] = 0
        else:
            self.__message_counter["path_total"]["_default"]

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
            if timedelta(seconds=remaining) > self.__message_counter_delay:
                self.__stats(force=True)

            time.sleep(remaining)
            self.__handle_sighup()
            remaining = self.rate_limit - (time.time() - starttime)

    def __del__(self):
        return self.stop(exitcode=0)

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
        else:
            self.__log('info', 'Bot stopped.')
            self.__print_log_buffer()

        if not getattr(self, 'testing', False) and self._standalone:
            sys.exit(exitcode)

        # in library-mode raise an error if e.g. initialization failed
        if exitcode != 0 and not self._standalone and not getattr(self, 'testing', False):
            raise ValueError('Bot shutdown. See error messages in logs for details.')

    def __print_log_buffer(self):
        for level, message in self.__log_buffer:
            if self.logger:
                getattr(self.logger, level)(message)
            if level in ['WARNING', 'ERROR', 'critical']:
                print(level.upper(), '-', message, file=sys.stderr)
            else:
                print(level.upper(), '-', message)
        self.__log_buffer = []

    def __check_bot_id(self, name: str) -> Tuple[str, str, str]:
        res = re.fullmatch(r'([0-9a-zA-Z\-]+)(\.[0-9]+)?', name)
        if res:
            if not (res.group(2) and threading.current_thread() == threading.main_thread()):
                return name, res.group(1), res.group(2)[1:] if res.group(2) else None
        self.__log('error',
                   "Invalid bot id, must match '"
                   r"[^0-9a-zA-Z\-]+'.")
        self.stop()
        return False, False, False

    def __connect_pipelines(self):
        pipeline_args = {key: getattr(self, key) for key in dir(self) if not inspect.ismethod(getattr(self, key)) and (key.startswith('source_pipeline_') or key.startswith('destination_pipeline'))}
        if self.source_queue is not None:
            self.logger.info("Loading source pipeline and queue %r.", self.source_queue)
            self.__source_pipeline = PipelineFactory.create(logger=self.logger,
                                                            direction="source",
                                                            queues=self.source_queue,
                                                            pipeline_args=pipeline_args,
                                                            load_balance=self.load_balance,
                                                            is_multithreaded=self.is_multithreaded)

            self.__source_pipeline.connect()
            self.__current_message = None
            self.logger.info("Connected to source queue.")

        if self.destination_queues:
            self.logger.info("Loading destination pipeline and queues %r.", self.destination_queues)
            self.__destination_pipeline = PipelineFactory.create(logger=self.logger,
                                                                 direction="destination",
                                                                 queues=self.destination_queues,
                                                                 pipeline_args=pipeline_args,
                                                                 load_balance=self.load_balance,
                                                                 is_multithreaded=self.is_multithreaded)

            self.__destination_pipeline.connect()
            self.logger.info("Connected to destination queues.")
        else:
            self.logger.info("No destination queues to load.")

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

            # Message counter start
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
            # Message counter end

            if self.__pipeline_serialize_messages:
                raw_message = libmessage.MessageFactory.serialize(message)
                self.__destination_pipeline.send(raw_message, path=path,
                                                 path_permissive=path_permissive)
            else:
                print(f'send_message, message: {message!r}')
                self.__destination_pipeline.send(message, path=path,
                                                 path_permissive=path_permissive)

    def receive_message(self) -> libmessage.Message:
        """


        If the bot is reloaded when waiting for an incoming message, the received message
        will be rejected to the pipeline in the first place to get to a clean state.
        Then, after reloading, the message will be retrieved again.
        """
        if self.__current_message is not None:
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
        if self.__sighup and self.__sighup.is_set():
            self.__source_pipeline.reject_message()
            self.__handle_sighup()
            return self.receive_message()

        try:
            if self.__pipeline_serialize_messages:
                self.__current_message = libmessage.MessageFactory.unserialize(message,
                                                                               harmonization=self.harmonization)
            else:
                self.__current_message = message

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

    def __load_configuration(self):
        self.__log('debug', "Loading runtime configuration from %r.", RUNTIME_CONF_FILE)
        if not self.__runtime_settings:
            try:
                self.__runtime_settings = utils.get_runtime()
            except ValueError:
                if not self._standalone:
                    self.__log('info', 'Could not load runtime configuration file. '
                               'Continuing, as we in library-mode.')
                    self.__runtime_settings = {}
                else:
                    raise

        # merge in configuration provided as parameter to init
        if self.__settings:
            if self.__bot_id not in self.__runtime_settings:
                self.__runtime_settings[self.__bot_id] = {}
            if 'parameters' not in self.__runtime_settings[self.__bot_id]:
                self.__runtime_settings[self.__bot_id]['parameters'] = {}
            self.__runtime_settings[self.__bot_id]['parameters'].update(self.__settings)

        for option, value in self.__runtime_settings.get('global', {}).items():
            setattr(self, option, value)
            self.__log_configuration_parameter("defaults", option, value)

        if self.__bot_id in self.__runtime_settings:
            params = self.__runtime_settings[self.__bot_id]
            for key, value in params.items():
                if key in ALLOWED_SYSTEM_PARAMETERS and value:
                    self.__log_configuration_parameter("system", key, value)
                    setattr(self, key, value)
                elif key not in IGNORED_SYSTEM_PARAMETERS:
                    self.__log('warning', 'Ignoring disallowed system parameter %r.',
                               key)
            for option, value in params.get('parameters', {}).items():
                setattr(self, option, value)
                self.__log_configuration_parameter("runtime", option, value)
        else:
            self.__log('warning', 'Bot ID %r not found in runtime configuration - could not load any parameters.',
                       self.__bot_id)

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

        self.__log_processed_messages_seconds = timedelta(seconds=self.log_processed_messages_seconds)

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

    def __log(self, level, message, *args, **kwargs):
        """
        If the logger is already initialized, redirect to the logger
        othwise write the message to the log buffer
        """
        if self.logger:
            getattr(self.logger, level)(message, *args, **kwargs)
        else:
            # we can't process **kwargs here, but not needed at this stage
            # if the message contains '%Y' or similar (e.g. a formatted `http_url`) but not args for formatting, no formatting should be done. if we did it, a wrong 'TypeError: not enough arguments for format string' would be thrown
            self.__log_buffer.append((level, message % args if args else message))

    def __log_configuration_parameter(self, config_name: str, option: str, value: Any):
        if "password" in option or "token" in option:
            value = "HIDDEN"

        message = f"{config_name.title()} configuration: parameter {option!r} loaded with value {value!r}."

        self.__log('debug', message)

    def __load_harmonization_configuration(self):
        self.logger.debug("Loading Harmonization configuration from %r.", HARMONIZATION_CONF_FILE)
        try:
            self._harmonization = utils.load_configuration(HARMONIZATION_CONF_FILE)
        except ValueError:
            if self._standalone:
                raise
            else:
                self._harmonization = utils.load_configuration(resource_filename('intelmq', 'etc/harmonization.conf'))

    def new_event(self, *args, **kwargs):
        return libmessage.Event(*args, harmonization=self.harmonization, **kwargs)

    @classmethod
    def run(cls, parsed_args=None):

        if not parsed_args:
            parsed_args = cls._create_argparser().parse_args()

        if not parsed_args.bot_id:
            sys.exit('No bot ID given.')

        instance = cls(parsed_args.bot_id, standalone=True)
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

    def process_message(self, *messages: Union[libmessage.Message, dict]):
        """
        Call the bot's process method with a prepared source queue.
        Return value is a dict with the complete pipeline state.
        Multiple messages can be given as positional argument.
        The pipeline needs to be configured accordinglit with BotLibSettings,
        see https://intelmq.readthedocs.io/en/develop/dev/library.html

        Access the output queue e.g. with return_value['output']
        """
        if self.bottype == BotType.COLLECTOR:
            if messages:
                raise exceptions.InvalidArgument('Collector Bots take no messages as processing input')
        else:
            # reset source queue
            self.__source_pipeline.state[self.source_queue] = []
            # reset internal queue
            if self.__source_pipeline._has_message:
                self.__source_pipeline.acknowledge()
            self.__current_message = None

            for message in messages:
                # convert to Message objects, it the message is a dict
                # use an appropriate default message type, not requiring __type keys in the message
                if not isinstance(message, libmessage.Message) and isinstance(message, dict):
                    message = libmessage.MessageFactory.from_dict(message=message,
                                                                  harmonization=self.harmonization,
                                                                  default_type=self._default_message_type)
                self.__source_pipeline.state[self.source_queue].append(message)
        # do not dump to file
        self.error_dump_message = False
        # do not serialize messages to strings, keep the objects
        self.__pipeline_serialize_messages = False

        # process all input messages
        while self.__source_pipeline.state[self.source_queue]:
            self.process()

        # clear destination state, before make a copy for return
        state = self.__destination_pipeline.state.copy()
        self.__destination_pipeline.clear_all_queues()

        return state


class ParserBot(Bot):
    bottype = BotType.PARSER
    _csv_params = {}
    _ignore_lines_starting = []
    _handle = None
    _current_line: Optional[str] = None
    _line_ending = '\r\n'
    _default_message_type = 'Report'

    default_fields: Optional[dict] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__class__.__name__ == 'ParserBot':
            self.logger.error('ParserBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()
        self.group = 'Parser'

        # validate default fields
        stop = False
        if self.default_fields:
            dummy_event = self.new_event()
            for key, value in self.default_fields.items():
                try:
                    dummy_event.add(key, value, raise_failure=True)

                except exceptions.InvalidValue:
                    self.logger.error("Invalid value of key '%s' in default_fields parameter.", key)
                    stop = True

                except exceptions.InvalidKey:
                    self.logger.error("Invalid key '%s' in default_fields parameter.", key)
                    stop = True

            if stop:
                self.stop()

    def _line_filtering_condition(self, line: str) -> str:
        return not any([line.startswith(prefix) for prefix in self._ignore_lines_starting])

    def _get_io_and_save_line_ending(self, raw: str) -> io.StringIO:
        """Prepare StringIO and save the original line ending

        The line ending is saved in self._line_ending. The default value is \\r\\n,
        the same as default used by csv module"""
        data_io = io.StringIO(raw, newline='')  # preserve original line ending
        self._line_ending = data_io.newlines

        # In case of mixed endings, StringIO will report a tuple with them.
        # In such a case, use the line ending default for the csv module
        if not self._line_ending or isinstance(self._line_ending, tuple):
            self._line_ending = '\r\n'
        return data_io

    def parse_csv(self, report: libmessage.Report):
        """
        A basic CSV parser.
        The resulting lines are lists.
        """
        raw_report: str = utils.base64_decode(report.get("raw")).strip()
        raw_report = raw_report.translate({0: None})
        report_io = self._get_io_and_save_line_ending(raw_report)
        if self._ignore_lines_starting:
            self._handle = RewindableFileHandle(report_io, condition=self._line_filtering_condition)
        else:
            self._handle = RewindableFileHandle(report_io)

        for line in csv.reader(self._handle, **self._csv_params):
            self._current_line = self._handle.current_line
            yield line

    def parse_csv_dict(self, report: libmessage.Report):
        """
        A basic CSV Dictionary parser.
        The resulting lines are dictionaries with the column names as keys.
        """
        raw_report: str = utils.base64_decode(report.get("raw")).strip()
        raw_report: str = raw_report.translate({0: None})
        report_io = self._get_io_and_save_line_ending(raw_report)
        if self._ignore_lines_starting:
            self._handle = RewindableFileHandle(report_io, condition=self._line_filtering_condition)
        else:
            self._handle = RewindableFileHandle(report_io)

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
        yield from json.loads(raw_report)

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
            if self._line_filtering_condition(line):
                self._current_line = line
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

                if self.default_fields:
                    for event in events:
                        for key, value in self.default_fields.items():
                            event.add(key, value, overwrite=False)

            except Exception:
                self.logger.exception('Failed to parse line.')
                self.__failed.append((traceback.format_exc(), self._current_line))
            else:
                events_count += len(events)
                self.send_message(*events)

        for exc, original_line in self.__failed:
            report_dump: libmessage.Message = report.copy()
            report_dump.change('raw', self.recover_line(original_line))
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

        Parameters:
            line (Optional[str], optional):
                The currently process line which should be transferred into it's
                original appearance. As fallback, "self._current_line" is used if
                available (depending on self.parse).
                The default is None.

        Raises:
            ValueError:
                If neither the parameter "line" nor the member "self._current_line"
                is available.

        Returns:
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

    def recover_line_csv(self, line: Optional[list] = None) -> str:
        """
        Recover csv line, respecting saved line ending.

        Parameter:
            line: Optional line as list. If absent, the current line is used as string.
        """
        if line:
            out = io.StringIO(newline='')
            writer = csv.writer(out, **{"lineterminator": self._line_ending, **self._csv_params})
            writer.writerow(line)
            result = out.getvalue()
        else:
            result = self._current_line
        return self._line_ending.join((self.tempdata or []) + [result])

    def recover_line_csv_dict(self, line: Union[dict, str, None] = None) -> str:
        """
        Converts dictionaries to csv. self.csv_fieldnames must be list of fields. Respect
        saved line ending.
        """
        out = io.StringIO(newline='')
        writer = csv.DictWriter(out, self.csv_fieldnames,
                                **{"lineterminator": self._line_ending, **self._csv_params})
        writer.writeheader()
        if isinstance(line, dict):
            writer.writerow(line)
        elif isinstance(line, str):
            out.write(line)
        else:
            out.write(self._current_line)

        return out.getvalue().strip()

    def recover_line_json(self, line: dict) -> str:
        """
        Reverse of parse for JSON pulses.

        Recovers a fully functional report with only the problematic pulse.
        Using a string as input here is not possible, as the input may span over multiple lines.
        Output is not identical to the input, but has the same content.

        Parameters:
            The line as dict.

        Returns:
            str: The JSON-encoded line as string.
        """
        return json.dumps([line])

    def recover_line_json_stream(self, line: Optional[str] = None) -> str:
        """
        recover_line for JSON streams (one JSON element per line, no outer structure),
        just returns the current line, unparsed.

        Parameters:
            line: The line itself as dict, if available, falls back to original current line

        Returns:
            str: unparsed JSON line.
        """
        return line if line else self._current_line


class CollectorBot(Bot):
    """
    Base class for collectors.

    Does some sanity checks on message sending.
    """

    bottype = BotType.COLLECTOR
    _is_multithreadable: bool = False
    name: Optional[str] = None
    accuracy: int = 100
    code: Optional[str] = None
    provider: Optional[str] = None
    documentation: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        return libmessage.Report(harmonization=self.harmonization)


class ExpertBot(Bot):
    """
    Base class for expert bots.
    """
    bottype = BotType.EXPERT
    _default_message_type = 'Event'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OutputBot(Bot):
    """
    Base class for outputs.
    """
    bottype = BotType.OUTPUT
    _default_message_type = 'Event'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__class__.__name__ == 'OutputBot':
            self.logger.error('OutputBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()
        self.group = 'Output'

        self.hierarchical: bool = getattr(self, "hierarchical_output",  # file and files
                                          getattr(self, "message_hierarchical",  # stomp and amqp code
                                                  getattr(self, "message_hierarchical_output", False)))  # stomp and amqp docs
        # some bots use the attribute `message_with_type`, others use `with_type`
        # this should be harmonized at some point
        self.with_type: bool = getattr(self, "message_with_type", getattr(self, "with_type", False))

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


class Parameters:
    pass


BotLibSettings = Dict39({'logging_path': None,
                         'source_pipeline_broker': 'Pythonlistsimple',
                         'destination_pipeline_broker': 'Pythonlistsimple',
                         'destination_queues': {'_default': 'output',
                                                '_on_error': 'error'}})
