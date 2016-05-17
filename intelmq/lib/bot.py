# -*- coding: utf-8 -*-
"""

"""

import datetime
import json
import re
import requests
import os
import signal
import sys
import time
import traceback

from intelmq import (DEFAULT_LOGGING_LEVEL, DEFAULT_LOGGING_PATH,
                     DEFAULTS_CONF_FILE, HARMONIZATION_CONF_FILE,
                     PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, SYSTEM_CONF_FILE)
from intelmq.lib import exceptions, utils
from intelmq.lib.message import MessageFactory
from intelmq.lib.pipeline import PipelineFactory

__all__ = ['Bot']


class Bot(object):

    def __init__(self, bot_id):
        self.__log_buffer = []
        self.parameters = Parameters()

        self.__current_message = None
        self.__last_message = None
        self.__message_counter = 0
        self.__error_retries_counter = 0
        self.__source_pipeline = None
        self.__destination_pipeline = None
        self.logger = None
        self.last_heartbeat = None

        try:
            version_info = sys.version.splitlines()[0].strip()
            self.__log_buffer.append(('info',
                                      '{} initialized with id {} and version '
                                      '{} as process {}.'
                                      ''.format(self.__class__.__name__,
                                                bot_id, version_info,
                                                os.getpid())))

            self.__load_defaults_configuration()
            self.__load_system_configuration()

            self.__check_bot_id(bot_id)
            self.__bot_id = bot_id

            if self.parameters.logging_handler == 'syslog':
                syslog = self.parameters.logging_syslog
            else:
                syslog = False
            self.logger = utils.log(self.__bot_id, syslog=syslog,
                                    log_level=self.parameters.logging_level)
        except:
            self.__log_buffer.append(('critical', traceback.format_exc()))
            self.stop()
        else:
            for line in self.__log_buffer:
                getattr(self.logger, line[0])(line[1])

        try:
            self.logger.info('Bot is starting.')
            self.__load_runtime_configuration()
            self.__load_pipeline_configuration()
            self.__load_harmonization_configuration()

            self.heartbeat_time = datetime.timedelta(seconds=self.parameters.bot_heartbeat_min_wait)

            self.init()

            signal.signal(signal.SIGHUP, self.__sighup)
        except:
            self.logger.exception('Bot initialization failed.')
            raise

    def __sighup(self, signum, stack):
        self.logger.info('Received SIGHUP, initializing again.')
        self.__disconnect_pipelines()
        self.logger.handlers = []  # remove all existing handlers
        self.__init__(self.__bot_id)
        self.__connect_pipelines()

    def init(self):
        pass

    def shutdown(self):
        pass

    def start(self, starting=True, error_on_pipeline=True,
              error_on_message=False, source_pipeline=None,
              destination_pipeline=None):
        self.__source_pipeline = source_pipeline
        self.__destination_pipeline = destination_pipeline
        self.logger.info('Bot starts processings.')

        while True:
            try:
                if not starting and (error_on_pipeline or error_on_message):
                    self.logger.info('Bot will restart in %s seconds.' %
                                     self.parameters.error_retry_delay)
                    time.sleep(self.parameters.error_retry_delay)
                    self.logger.info('Bot woke up')
                    self.logger.info('Trying to start processing again.')

                if error_on_message:
                    error_on_message = False

                if error_on_pipeline:
                    self.__connect_pipelines()
                    error_on_pipeline = False

                if starting:
                    self.logger.info("Start processing.")
                    starting = False

                self.process()
                self.__error_retries_counter = 0  # reset counter

                self.__source_pipeline.sleep(self.parameters.rate_limit)

            except exceptions.PipelineError:
                error_on_pipeline = True
                error_traceback = traceback.format_exc()

                if self.parameters.error_log_exception:
                    self.logger.exception('Pipeline failed.')
                else:
                    self.logger.error('Pipeline failed.')
                self.__disconnect_pipelines()

            except Exception:
                error_on_message = True
                error_traceback = traceback.format_exc()

                if self.parameters.error_log_exception:
                    self.logger.exception("Bot has found a problem.")
                else:
                    self.logger.error("Bot has found a problem.")

                if self.parameters.error_log_message:
                    self.logger.info("Last Correct Message(event): {!r}."
                                     "".format(self.__last_message)[:500])
                    self.logger.info("Current Message(event): {!r}."
                                     "".format(self.__current_message)[:500])

            except KeyboardInterrupt:
                self.logger.error("Received KeyboardInterrupt.")
                self.stop()
                break

            else:
                if (not self.last_heartbeat or
                        (datetime.datetime.now() - self.last_heartbeat) > self.heartbeat_time):
                    requests.get(self.parameters.bot_heartbeat_url.format(bot_id=self.bot_id))
                    self.last_heartbeat = datetime.datetime.now()

            finally:
                if self.parameters.testing:
                    self.stop()
                    break

                if error_on_message or error_on_pipeline:
                    self.__error_retries_counter += 1

                    # reached the maximum number of retries
                    if (self.__error_retries_counter >
                            self.parameters.error_max_retries):

                        if error_on_message:

                            if self.parameters.error_dump_message:
                                self.__dump_message(error_traceback)

                            # remove message from pipeline
                            self.acknowledge_message()

                            # when bot acknowledge the message,
                            # dont need to wait again
                            error_on_message = False

                        # error_procedure: stop
                        if self.parameters.error_procedure == "stop":
                            self.stop()

                        # error_procedure: pass
                        else:
                            self.__error_retries_counter = 0  # reset counter

    def __del__(self):
        self.stop()

    def stop(self):
        self.shutdown()

        self.__disconnect_pipelines()

        if self.logger:
            self.logger.info("Bot stopped.")
        else:
            self.__log_buffer.append(('info', 'Bot stopped.'))
            self.__print_log_buffer()

        if not self.parameters.testing:
            self.__terminate()

    def __terminate(self):
        try:
            self.logger.error("Exiting.")
        except:
            print("Exiting")
        exit(-1)

    def __print_log_buffer(self):
        for level, message in self.__log_buffer:
            if self.logger:
                getattr(self.logger, level)(message)
            print(level.upper(), '-', message)
        self.__log_buffer = []

    def __check_bot_id(self, str):
        res = re.search('[^0-9a-zA-Z\-]+', str)
        if res:
            self.__log_buffer.append(('error',
                                      "Invalid bot id, must match '"
                                      "[^0-9a-zA-Z\-]+'."))
            self.stop()

    def __connect_pipelines(self):
        self.logger.info("Loading source pipeline.")
        self.__source_pipeline = PipelineFactory.create(self.parameters)
        self.logger.info("Loading source queue.")
        self.__source_pipeline.set_queues(self.__source_queues, "source")
        self.logger.info("Source queue loaded {}."
                         "".format(self.__source_queues))
        self.__source_pipeline.connect()
        self.logger.info("Connected to source queue.")

        self.logger.info("Loading destination pipeline.")
        self.__destination_pipeline = PipelineFactory.create(self.parameters)
        self.logger.info("Loading destination queues.")
        self.__destination_pipeline.set_queues(self.__destination_queues,
                                               "destination")
        self.logger.info("Destination queues loaded {}."
                         "".format(self.__destination_queues))
        self.__destination_pipeline.connect()
        self.logger.info("Connected to destination queues.")

        self.logger.info("Pipeline ready.")

    def __disconnect_pipelines(self):
        """ Disconnecting pipelines. """
        if self.__source_pipeline:
            self.__source_pipeline.disconnect()
            self.__source_pipeline = None
            self.logger.info("Disconnecting from source pipeline.")
        if self.__destination_pipeline:
            self.__destination_pipeline.disconnect()
            self.__destination_pipeline = None
            self.logger.info("Disconnecting from destination pipeline.")

    def send_message(self, message):
        if not message:
            self.logger.warning("Sending Message: Empty message found.")
            return False

        self.logger.debug("Sending message.")
        self.__message_counter += 1
        if self.__message_counter % 500 == 0:
            self.logger.info("Processed %s messages." % self.__message_counter)

        raw_message = MessageFactory.serialize(message)
        self.__destination_pipeline.send(raw_message)

    def receive_message(self):
        self.logger.debug('Receiving Message.')
        message = None
        while not message:
            message = self.__source_pipeline.receive()
            if not message:
                self.logger.warning('Empty message received.')
                continue
            self.logger.debug('Receive message {!r}...'.format(message[:500]))

        self.__current_message = MessageFactory.unserialize(message)
        return self.__current_message

    def acknowledge_message(self):
        self.__last_message = self.__current_message
        self.__source_pipeline.acknowledge()

    def __dump_message(self, error_traceback):
        if self.__current_message is None:
            return

        self.logger.info('Dumping message from pipeline to dump file.')
        timestamp = datetime.datetime.utcnow()
        timestamp = timestamp.isoformat()

        dump_file = "%s%s.dump" % (self.parameters.logging_path, self.__bot_id)

        new_dump_data = dict()
        new_dump_data[timestamp] = dict()
        new_dump_data[timestamp]["bot_id"] = self.__bot_id
        new_dump_data[timestamp]["source_queue"] = self.__source_queues
        new_dump_data[timestamp]["traceback"] = error_traceback

        new_dump_data[timestamp]["message"] = self.__current_message.serialize()

        try:
            with open(dump_file, 'r') as fp:
                dump_data = json.load(fp)
                dump_data.update(new_dump_data)
        except:
            dump_data = new_dump_data

        with open(dump_file, 'w') as fp:
            json.dump(dump_data, fp, indent=4, sort_keys=True)

        self.logger.info('Message dumped.')
        self.__current_message = None

    def __load_defaults_configuration(self):
        self.__log_buffer.append(('debug', "Loading defaults configuration."))
        config = utils.load_configuration(DEFAULTS_CONF_FILE)

        setattr(self.parameters, 'testing', False)
        setattr(self.parameters, 'logging_path', DEFAULT_LOGGING_PATH)
        setattr(self.parameters, 'logging_level', DEFAULT_LOGGING_LEVEL)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.__log_buffer.append(('debug',
                                      "Defaults configuration: parameter '{}' "
                                      "loaded  with value '{}'.".format(option,
                                                                        value)))

    def __load_system_configuration(self):
        self.__log_buffer.append(('debug', "Loading system configuration"))
        config = utils.load_configuration(SYSTEM_CONF_FILE)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.__log_buffer.append(('debug',
                                      "System configuration: parameter '{}' "
                                      "loaded  with value '{}'.".format(option,
                                                                        value)))

    def __load_runtime_configuration(self):
        self.logger.debug("Loading runtime configuration")
        config = utils.load_configuration(RUNTIME_CONF_FILE)

        if self.__bot_id in list(config.keys()):
            for option, value in config[self.__bot_id].items():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter '%s' "
                                  "loaded with value '%s'." % (option, value))

    def __load_pipeline_configuration(self):
        self.logger.debug("Loading pipeline configuration")
        config = utils.load_configuration(PIPELINE_CONF_FILE)

        self.__source_queues = None
        self.__destination_queues = None

        if self.__bot_id in list(config.keys()):

            if 'source-queue' in config[self.__bot_id].keys():
                self.__source_queues = config[self.__bot_id]['source-queue']
                self.logger.debug("Pipeline configuration: parameter "
                                  "'source-queue' loaded with the value '%s'."
                                  % self.__source_queues)

            if 'destination-queues' in config[self.__bot_id].keys():

                self.__destination_queues = config[
                    self.__bot_id]['destination-queues']
                self.logger.debug("Pipeline configuration: parameter"
                                  "'destination-queues' loaded with the value "
                                  "'%s'." % ", ".join(self.__destination_queues))

        else:
            self.logger.error("Pipeline configuration: no key "
                              "'{}'.".format(self.__bot_id))
            self.stop()

    def __load_harmonization_configuration(self):
        self.logger.debug("Loading Harmonization configuration.")
        config = utils.load_configuration(HARMONIZATION_CONF_FILE)

        for message_types in config.keys():
            for key in config[message_types].keys():
                for _key in config.keys():
                    if _key.startswith("%s." % key):
                        raise exceptions.ConfigurationError(
                            'harmonization',
                            "Key %s is not valid." % _key)


class Parameters(object):
    pass
