# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function, unicode_literals

import datetime
import json
import re
import requests
import sys
import time
import traceback

from intelmq import (DEFAULT_LOGGING_LEVEL, DEFAULT_LOGGING_PATH,
                     DEFAULTS_CONF_FILE, HARMONIZATION_CONF_FILE,
                     PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, SYSTEM_CONF_FILE)
from intelmq.lib import exceptions, utils
from intelmq.lib.message import MessageFactory
from intelmq.lib.pipeline import PipelineFactory


class Bot(object):

    def __init__(self, bot_id):
        self.log_buffer = []
        self.parameters = Parameters()

        self.current_message = None
        self.last_message = None
        self.message_counter = 0
        self.error_retries_counter = 0
        self.source_pipeline = None
        self.destination_pipeline = None
        self.logger = None
        self.last_heartbeat = None

        try:
            version_info = sys.version.splitlines()[0].strip()
            self.log_buffer.append(('info',
                                    '{} initialized with id {} and version {}.'
                                    ''.format(self.__class__.__name__,
                                              bot_id, version_info)))
            self.check_bot_id(bot_id)
            self.bot_id = bot_id

            self.load_defaults_configuration()
            self.load_system_configuration()
            if self.parameters.logging_handler == 'syslog':
                syslog = self.parameters.logging_syslog
            else:
                syslog = False
            self.logger = utils.log(self.bot_id,
                                    log_level=self.parameters.logging_level)
#                                    syslog=syslog)
        except:
            self.log_buffer.append(('critical', traceback.format_exc()))
            self.stop()
        else:
            for line in self.log_buffer:
                getattr(self.logger, line[0])(line[1])

        try:
            self.logger.info('Bot is starting.')
            self.load_runtime_configuration()
            self.load_pipeline_configuration()
            self.load_harmonization_configuration()

            self.heartbeat_time = datetime.timedelta(seconds=self.parameters.bot_heartbeat_min_wait)

            self.init()
        except:
            self.logger.exception('Bot initialization failed.')
            raise

    def init(self):
        pass

    def start(self, starting=True, error_on_pipeline=True,
              error_on_message=False, source_pipeline=None,
              destination_pipeline=None):
        self.source_pipeline = source_pipeline
        self.destination_pipeline = destination_pipeline
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
                    self.connect_pipelines()
                    error_on_pipeline = False

                if starting:
                    self.logger.info("Start processing.")
                    starting = False

                self.process()
                self.error_retries_counter = 0  # reset counter

                self.source_pipeline.sleep(self.parameters.rate_limit)

            except exceptions.PipelineError:
                error_on_pipeline = True
                error_traceback = traceback.format_exc()

                if self.parameters.error_log_exception:
                    self.logger.exception('Pipeline failed.')
                else:
                    self.logger.error('Pipeline failed.')
                self.disconnect_pipelines()

            except Exception:
                error_on_message = True
                error_traceback = traceback.format_exc()

                if self.parameters.error_log_exception:
                    self.logger.exception("Bot has found a problem.")
                else:
                    self.logger.error("Bot has found a problem.")

                if self.parameters.error_log_message:
                    self.logger.info("Last Correct Message(event): {!r}."
                                     "".format(self.last_message)[:500])
                    self.logger.info("Current Message(event): {!r}."
                                     "".format(self.current_message)[:500])

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
                    self.error_retries_counter += 1

                    # reached the maximum number of retries
                    if (self.error_retries_counter >
                            self.parameters.error_max_retries):

                        if error_on_message:

                            if self.parameters.error_dump_message:
                                self.dump_message(error_traceback)

                            # FIXME: if broker fails in this instant
                            #        it will crash the bot
                            #
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
                            self.error_retries_counter = 0  # reset counter

    def stop(self):
        self.disconnect_pipelines()

        if self.logger:
            self.logger.info("Bot stopped.")
        else:
            self.log_buffer.append(('info', 'Bot stopped.'))
            self.print_log_buffer()

        if not self.parameters.testing:
            self.terminate()

    def terminate(self):
        try:
            self.logger.error("Exiting.")
        except:
            pass
        finally:
            print("Exiting")
        exit(-1)

    def print_log_buffer(self):
        for level, message in self.log_buffer:
            if self.logger:
                getattr(self.logger, level)(message)
            print(level.upper(), '-', message)
        self.log_buffer = []

    def check_bot_id(self, str):
        res = re.search('[^0-9a-zA-Z\-]+', str)
        if res:
            self.log_buffer.append(('error',
                                    "Invalid bot id, must match '"
                                    "[^0-9a-zA-Z\-]+'."))
            self.stop()

    def connect_pipelines(self):
        self.logger.info("Loading source pipeline.")
        self.source_pipeline = PipelineFactory.create(
            self.parameters)
        self.logger.info("Loading source queue.")
        self.source_pipeline.set_queues(self.source_queues,
                                        "source")
        self.logger.info("Source queue loaded {}."
                         "".format(self.source_queues))
        self.source_pipeline.connect()
        self.logger.info("Connected to source queue.")

        self.logger.info("Loading destination pipeline.")
        self.destination_pipeline = PipelineFactory.create(
            self.parameters)
        self.logger.info("Loading destination queues.")
        self.destination_pipeline.set_queues(self.destination_queues,
                                             "destination")
        self.logger.info("Destination queues loaded {}."
                         "".format(self.destination_queues))
        self.destination_pipeline.connect()
        self.logger.info("Connected to destination queues.")

        self.logger.info("Pipeline ready.")

    def disconnect_pipelines(self):
        """ Disconnecting pipelines. """
        if self.source_pipeline:
            self.source_pipeline.disconnect()
            self.source_pipeline = None
            self.logger.info("Disconnecting from source pipeline.")
        if self.destination_pipeline:
            self.destination_pipeline.disconnect()
            self.destination_pipeline = None
            self.logger.info("Disconnecting from destination pipeline.")

    def send_message(self, message):
        if not message:
            self.logger.warning("Sending Message: Empty message found.")
            return False

        self.logger.debug("Sending message.")
        self.message_counter += 1
        if self.message_counter % 500 == 0:
            self.logger.info("Processed %s messages." % self.message_counter)

        raw_message = MessageFactory.serialize(message)
        self.destination_pipeline.send(raw_message)

    def receive_message(self):
        self.logger.debug('Receiving Message.')
        message = self.source_pipeline.receive()

        self.logger.debug('Receive message {!r}...'.format(message[:500]))
        if not message:
            self.logger.warning('Empty message received.')
            return None

        self.current_message = MessageFactory.unserialize(message)
        return self.current_message

    def acknowledge_message(self):
        self.last_message = self.current_message
        self.source_pipeline.acknowledge()

    def dump_message(self, error_traceback):
        if self.current_message is None:
            return

        self.logger.info('Dumping message from pipeline to dump file.')
        timestamp = datetime.datetime.utcnow()
        timestamp = timestamp.isoformat()

        dump_file = "%s%s.dump" % (self.parameters.logging_path, self.bot_id)

        new_dump_data = dict()
        new_dump_data[timestamp] = dict()
        new_dump_data[timestamp]["bot_id"] = self.bot_id
        new_dump_data[timestamp]["source_queue"] = self.source_queues
        new_dump_data[timestamp]["traceback"] = error_traceback

        new_dump_data[timestamp]["message"] = self.current_message.serialize()

        try:
            with open(dump_file, 'r') as fp:
                dump_data = json.load(fp)
                dump_data.update(new_dump_data)
        except:
            dump_data = new_dump_data

        with open(dump_file, 'w') as fp:
            json.dump(dump_data, fp, indent=4, sort_keys=True)

        self.logger.info('Message dumped.')
        self.current_message = None


    def load_defaults_configuration(self):
        self.log_buffer.append(('debug', "Loading defaults configuration."))
        config = utils.load_configuration(DEFAULTS_CONF_FILE)

        setattr(self.parameters, 'testing', False)
        setattr(self.parameters, 'logging_path', DEFAULT_LOGGING_PATH)
        setattr(self.parameters, 'logging_level', DEFAULT_LOGGING_LEVEL)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.log_buffer.append(('debug',
                                    "Defaults configuration: parameter '{}' "
                                    "loaded  with value '{}'.".format(option,
                                                                      value)))

    def load_system_configuration(self):
        self.log_buffer.append(('debug', "Loading system configuration"))
        config = utils.load_configuration(SYSTEM_CONF_FILE)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.log_buffer.append(('debug',
                                    "System configuration: parameter '{}' "
                                    "loaded  with value '{}'.".format(option,
                                                                      value)))

    def load_runtime_configuration(self):
        self.logger.debug("Loading runtime configuration")
        config = utils.load_configuration(RUNTIME_CONF_FILE)

        if self.bot_id in list(config.keys()):
            for option, value in config[self.bot_id].items():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter '%s' "
                                  "loaded with value '%s'." % (option, value))

    def load_pipeline_configuration(self):
        self.logger.debug("Loading pipeline configuration")
        config = utils.load_configuration(PIPELINE_CONF_FILE)

        self.source_queues = None
        self.destination_queues = None

        if self.bot_id in list(config.keys()):

            if 'source-queue' in config[self.bot_id].keys():
                self.source_queues = config[self.bot_id]['source-queue']
                self.logger.debug("Pipeline configuration: parameter "
                                  "'source-queue' loaded with the value '%s'."
                                  % self.source_queues)

            if 'destination-queues' in config[self.bot_id].keys():

                self.destination_queues = config[
                    self.bot_id]['destination-queues']
                self.logger.debug("Pipeline configuration: parameter"
                                  "'destination-queues' loaded with the value "
                                  "'%s'." % ", ".join(self.destination_queues))

        else:
            self.logger.error("Pipeline configuration: no key "
                              "'{}'.".format(self.bot_id))
            self.stop()

    def load_harmonization_configuration(self):
        self.logger.debug("Loading Harmonization configuration.")
        config = utils.load_configuration(HARMONIZATION_CONF_FILE)

        for message_types in config.keys():
            for key in config[message_types].keys():
                for _key in config.keys():
                    if _key.startswith("%s." % key):
                        # FIXME: write in devguide the rules for the keys names
                        raise exceptions.ConfigurationError(
                            'harmonization',
                            "Key %s is not valid." % _key)


class Parameters(object):
    pass
