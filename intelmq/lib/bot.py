# -*- coding: utf-8 -*-
"""

"""

import csv
import datetime
import io
import json
import re
import requests
import os
import signal
import sys
import time
import traceback

from intelmq import (DEFAULT_LOGGING_PATH,
                     DEFAULTS_CONF_FILE, HARMONIZATION_CONF_FILE,
                     PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, SYSTEM_CONF_FILE)
from intelmq.lib import exceptions, utils
from intelmq.lib.message import MessageFactory
from intelmq.lib.pipeline import PipelineFactory

__all__ = ['Bot', 'ParserBot']


class Bot(object):

    def __init__(self, bot_id):
        self.__log_buffer = []
        self.parameters = Parameters()

        self.__current_message = None
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
                                    log_path=self.parameters.logging_path,
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

                if self.parameters.rate_limit:
                    self.logger.info("Idling for {!s}s now.".format(self.parameters.rate_limit))
                    time.sleep(self.parameters.rate_limit)

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
                    # Dump full message if explicitly requested by config
                    self.logger.info("Current Message(event): {!r}."
                                     "".format(self.__current_message))

            except KeyboardInterrupt:
                self.logger.error("Received KeyboardInterrupt.")
                self.stop()
                break

            else:
                if (not self.last_heartbeat or
                        (datetime.datetime.now() - self.last_heartbeat) > self.heartbeat_time):
                    requests.get(self.parameters.bot_heartbeat_url.format(bot_id=self.__bot_id))
                    self.last_heartbeat = datetime.datetime.now()

            finally:
                if getattr(self.parameters, 'testing', False):
                    self.stop()
                    break

                if error_on_message or error_on_pipeline:
                    self.__error_retries_counter += 1

                    # reached the maximum number of retries
                    if (self.__error_retries_counter >
                            self.parameters.error_max_retries):

                        if error_on_message:

                            if self.parameters.error_dump_message:
                                self._dump_message(error_traceback,
                                                   message=self.__current_message)
                                self.__current_message = None

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

        if not getattr(self.parameters, 'testing', False):
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
        self.logger.debug("Loading source pipeline.")
        self.__source_pipeline = PipelineFactory.create(self.parameters)
        self.logger.debug("Loading source queue.")
        self.__source_pipeline.set_queues(self.__source_queues, "source")
        self.logger.debug("Source queue loaded {}."
                          "".format(self.__source_queues))
        self.__source_pipeline.connect()
        self.logger.debug("Connected to source queue.")

        self.logger.debug("Loading destination pipeline.")
        self.__destination_pipeline = PipelineFactory.create(self.parameters)
        self.logger.debug("Loading destination queues.")
        self.__destination_pipeline.set_queues(self.__destination_queues,
                                               "destination")
        self.logger.debug("Destination queues loaded {}."
                          "".format(self.__destination_queues))
        self.__destination_pipeline.connect()
        self.logger.debug("Connected to destination queues.")

        self.logger.info("Pipeline ready.")

    def __disconnect_pipelines(self):
        """ Disconnecting pipelines. """
        if self.__source_pipeline:
            self.__source_pipeline.disconnect()
            self.__source_pipeline = None
            self.logger.debug("Disconnecting from source pipeline.")
        if self.__destination_pipeline:
            self.__destination_pipeline.disconnect()
            self.__destination_pipeline = None
            self.logger.debug("Disconnecting from destination pipeline.")

    def send_message(self, *messages):
        for message in messages:
            if not message:
                self.logger.warning("Ignoring empty message at sending.")
                continue

            self.logger.debug("Sending message.")
            self.__message_counter += 1
            if self.__message_counter % 500 == 0:
                self.logger.info("Processed %s messages." % self.__message_counter)

            raw_message = MessageFactory.serialize(message)
            self.__destination_pipeline.send(raw_message)

    def receive_message(self):
        self.logger.debug('Waiting for incoming message.')
        message = None
        while not message:
            message = self.__source_pipeline.receive()
            if not message:
                self.logger.warning('Empty message received.')
                continue
        self.__current_message = MessageFactory.unserialize(message)

        if 'raw' in self.__current_message and len(self.__current_message['raw']) > 400:
            tmp_msg = self.__current_message.to_dict(hierarchical=False)
            tmp_msg['raw'] = tmp_msg['raw'][:397] + '...'
        else:
            tmp_msg = self.__current_message
        self.logger.debug('Received message {!r}.'.format(tmp_msg))

        return self.__current_message

    def acknowledge_message(self):
        self.__source_pipeline.acknowledge()

    def _dump_message(self, error_traceback, message):
        if message is None:
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

        new_dump_data[timestamp]["message"] = message.serialize()

        try:
            with open(dump_file, 'r') as fp:
                dump_data = json.load(fp)
                dump_data.update(new_dump_data)
        except:
            dump_data = new_dump_data

        with open(dump_file, 'w') as fp:
            json.dump(dump_data, fp, indent=4, sort_keys=True)

        self.logger.warn('Message dumped.')

    def __load_defaults_configuration(self):
        self.__log_buffer.append(('debug', "Loading defaults configuration."))
        config = utils.load_configuration(DEFAULTS_CONF_FILE)

        setattr(self.parameters, 'logging_path', DEFAULT_LOGGING_PATH)

        for option, value in config.items():
            setattr(self.parameters, option, value)
            self.__log_buffer.append(('debug',
                                      "Defaults configuration: parameter {!r} "
                                      "loaded  with value {!r}.".format(option,
                                                                        value)))

    def __load_system_configuration(self):
        if os.path.exists(SYSTEM_CONF_FILE):
            self.__log_buffer.append(('warning', "system.conf is deprecated and will be"
                                      "removed in 1.0. Use defaults.conf instead!"))
            self.__log_buffer.append(('debug', "Loading system configuration."))
            config = utils.load_configuration(SYSTEM_CONF_FILE)

            for option, value in config.items():
                setattr(self.parameters, option, value)
                self.__log_buffer.append(('debug',
                                          "System configuration: parameter {!r} "
                                          "loaded  with value {!r}.".format(option, value)))

    def __load_runtime_configuration(self):
        self.logger.debug("Loading runtime configuration.")
        config = utils.load_configuration(RUNTIME_CONF_FILE)

        if self.__bot_id in list(config.keys()):
            for option, value in config[self.__bot_id].items():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter {!r} "
                                  "loaded with value {!r}.".format(option, value))

    def __load_pipeline_configuration(self):
        self.logger.debug("Loading pipeline configuration.")
        config = utils.load_configuration(PIPELINE_CONF_FILE)

        self.__source_queues = None
        self.__destination_queues = None

        if self.__bot_id in list(config.keys()):

            if 'source-queue' in config[self.__bot_id].keys():
                self.__source_queues = config[self.__bot_id]['source-queue']
                self.logger.debug("Pipeline configuration: parameter "
                                  "'source-queue' loaded with the value {!r}."
                                  "".format(self.__source_queues))

            if 'destination-queues' in config[self.__bot_id].keys():

                self.__destination_queues = config[
                    self.__bot_id]['destination-queues']
                self.logger.debug("Pipeline configuration: parameter"
                                  "'destination-queues' loaded with the value "
                                  "{!r}.".format(", ".join(self.__destination_queues)))

        else:
            self.logger.error("Pipeline configuration: no key "
                              "{!r}.".format(self.__bot_id))
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


class ParserBot(Bot):

    def __init__(self, bot_id):
        super(ParserBot, self).__init__(bot_id=bot_id)
        if self.__class__.__name__ == 'ParserBot':
            self.logger.error('ParserBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()

    def parse_csv(self, report):
        """
        A basic CSV parser.
        """
        raw_report = utils.base64_decode(report.get("raw"))
        for line in csv.reader(io.StringIO(raw_report)):
            yield line

    def parse(self, report):
        """
        A generator yielding the single elements of the data.

        Comments, headers etc. can be processed here. Data needed by
        `self.parse_line` can be saved in `self.tempdata` (list).

        Default parser yields stripped lines.
        Override for your use or use an exisiting parser, e.g.:
            parse = ParserBot.parse_csv
        """
        for line in utils.base64_decode(report.get("raw")).splitlines():
            yield line.strip()

    def parse_line(self, line, report):
        """
        A generator which can yield one or more messages contained in line.

        Report has the full message, thus you can access some metadata.
        Override for your use.
        """
        raise NotImplementedError

    def process(self):
        self.tempdata = []  # temporary data for parse, parse_line and recover_line
        self.__failed = []
        report = self.receive_message()

        if 'raw' not in report:
            self.logger.warning('Report without raw field received. Possible '
                                'bug or misconfiguration in previous bots.')
            self.acknowledge_message()
            return

        for line in self.parse(report):
            if not line:
                continue
            try:
                # filter out None
                events = list(filter(bool, self.parse_line(line, report)))
            except Exception:
                self.logger.exception('Failed to parse line.')
                self.__failed.append((traceback.format_exc(), line))
            else:
                self.send_message(*events)

        for exc, line in self.__failed:
            report_dump = report.copy()
            report_dump.update('raw', self.recover_line(line))
            self._dump_message(exc, report_dump)

        self.acknowledge_message()

    def recover_line(self, line):
        """
        Reverse of parse for single lines.

        Recovers a fully functional report with only the problematic line.
        """
        return '\n'.join(self.tempdata + [line])

    def recover_line_csv(self, line):
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(line)
        return out.getvalue()

    csv_params = {}

    def recover_line_csv_dict(self, line):
        """
        Converts dictionaries to csv. self.csv_fieldnames must be list of fields.
        """
        out = io.StringIO()
        writer = csv.DictWriter(out, self.csv_fieldnames, **self.csv_params)
        writer.writeheader()
        writer.writerow(line)
        return out.getvalue()


class CollectorBot(Bot):
    """
    Base class for collectors.

    Does some sanity checks on message sending.
    """
    def __init__(self, bot_id):
        super(CollectorBot, self).__init__(bot_id=bot_id)
        if self.__class__.__name__ == 'CollectorBot':
            self.logger.error('CollectorBot can\'t be started itself. '
                              'Possible Misconfiguration.')
            self.stop()

    def __filter_empty_report(self, message):
        if 'raw' not in message:
            self.logger.warning('Ignoring report without raw field. '
                                'Possible bug or miconfiguration of this bot.')
            return False
        return True

    def __add_report_fields(self, report):
        report.add("feed.name", self.parameters.feed)
        if hasattr(self.parameters, 'code'):
            report.add("feed.code", self.parameters.code)
        report.add("feed.accuracy", self.parameters.accuracy)
        return report

    def send_message(self, *messages):
        messages = filter(self.__filter_empty_report, messages)
        messages = map(self.__add_report_fields, messages)
        super(CollectorBot, self).send_message(*messages)


class Parameters(object):
    pass
