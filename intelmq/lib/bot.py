import re
import sys
import json
import time
import datetime
import traceback
import ConfigParser

from intelmq import SYSTEM_CONF_FILE
from intelmq import STARTUP_CONF_FILE
from intelmq import RUNTIME_CONF_FILE
from intelmq import DEFAULTS_CONF_FILE
from intelmq import PIPELINE_CONF_FILE
from intelmq import HARMONIZATION_CONF_FILE
from intelmq import DEFAULT_LOGGING_PATH
from intelmq import DEFAULT_LOGGING_LEVEL

from intelmq.lib import utils
from intelmq.lib import exceptions
from intelmq.lib.message import MessageFactory
from intelmq.lib.pipeline import PipelineFactory


class Bot(object):

    def __init__(self, bot_id):
        self.parameters = Parameters()

        self.current_message = None
        self.last_message = None
        self.message_counter = 0
        self.error_retries_counter = 0

        self.check_bot_id(bot_id)
        self.bot_id = bot_id

        self.load_system_configuration()

        self.logger = utils.log(
                                self.parameters.logging_path,
                                self.bot_id,
                                self.parameters.logging_level
                               )
        self.logger.info('Bot is starting')

        self.load_defaults_configuration()
        self.load_runtime_configuration()
        self.load_pipeline_configuration()
        self.load_harmonization_configuration()

        self.init()

    def init(self):
        pass

    def start(self):
        self.source_pipeline = None
        self.destination_pipeline = None

        starting = True
        error_on_pipeline = True
        error_on_message = False

        self.logger.info('Bot start processing')

        while True:
            try:
                if not starting and (error_on_pipeline or error_on_message):
                    self.logger.info('Bot will restart in %s seconds' % self.parameters.error_retry_delay)
                    time.sleep(self.parameters.error_retry_delay)
                    self.logger.info('Bot woke up')
                    self.logger.info('Trying to start processing again')

                if error_on_message:
                    error_on_message = False

                if error_on_pipeline:
                    self.logger.info("Loading source pipeline")

                    self.source_pipeline = PipelineFactory.create(self.parameters)
                    self.logger.info("Loading source queue")
                    self.source_pipeline.set_queues(self.source_queues, "source")
                    self.logger.info("Source queue loaded")
                    self.source_pipeline.connect()
                    self.logger.info("Connected to source queue")

                    self.destination_pipeline = PipelineFactory.create(self.parameters)
                    self.logger.info("Loading destination queues")
                    self.destination_pipeline.set_queues(self.destination_queues, "destination")
                    self.logger.info("Destination queues loaded")
                    self.destination_pipeline.connect()
                    self.logger.info("Connected to destination queues")

                    self.logger.info("Pipeline ready")
                    error_on_pipeline = False

                if starting:
                    self.logger.info("Start processing")
                    starting = False

                self.process()
                self.source_pipeline.sleep(self.parameters.rate_limit)

            except exceptions.PipelineError, ex:
                error_on_pipeline = True
                self.logger.error('Pipeline failed')
                self.logger.exception("Check the following exception: \n%s" % ex)
                self.source_pipeline = None
                self.destination_pipeline = None

            except Exception, ex:
                self.logger.error("Bot has found a problem")
                self.logger.exception(ex)

                if self.parameters.error_procedure == "retry":
                    if self.parameters.error_max_retries <= 0:
                        pass

                    # FIXME: number of retries is wrong + 1 please!
                    elif self.error_retries_counter < self.parameters.error_max_retries:
                        self.error_retries_counter += 1

                    elif self.error_retries_counter >= self.parameters.error_max_retries:
                        if self.parameters.error_dump_message:
                            self.dump_message(ex)
                            self.acknowledge_message()
                        else:
                            self.acknowledge_message()

                    else:
                        pass

                    # when bot acknowledge the message, dont need to wait again
                    error_on_message = True

                else:  # error_procedure == "pass"
                    if self.parameters.error_dump_message:
                        self.dump_message(ex)
                    self.acknowledge_message()

                if self.parameters.error_log_exception:
                    self.logger.exception("Check the following exception: \n%s" % ex)

                if self.parameters.error_log_message:
                    self.logger.info("Last Correct Message(event): %r" % self.last_message)  # FIXME: evaluate if its ok
                    self.logger.info("Current Message(event): %r" % self.current_message)    # FIXME: evaluate if its ok

            except KeyboardInterrupt as e:
                if self.source_pipeline:
                    self.source_pipeline.disconnect()
                    self.logger.info("Disconnecting from source pipeline")
                if self.destination_pipeline:
                    self.destination_pipeline.disconnect()
                    self.logger.info("Disconnecting from destination pipeline")

                self.logger.info("Bot is shutting down")
                break

    def stop(self):
        try:
            self.logger.error("Bot found an error. Exiting")
        except:
            pass
        finally:
            print "Bot found an error. Exiting"
        exit(-1)

    def check_bot_id(self, str):
        res = re.search('[^0-9a-zA-Z\-]+', str)
        if res:
            print "Invalid bot id."
            self.stop()

    def send_message(self, message):
        if not message:
            self.logger.debug("Empty message found.")
            return False

        self.message_counter += 1
        if self.message_counter % 500 == 0:
            self.logger.info("Processed %s messages" % self.message_counter)

        raw_message = MessageFactory.serialize(message)
        self.destination_pipeline.send(raw_message)

    def receive_message(self):
        message = self.source_pipeline.receive()

        if not message:
            return None

        self.current_message = MessageFactory.unserialize(message)
        return self.current_message

    def acknowledge_message(self):
        self.last_message = self.current_message
        self.source_pipeline.acknowledge()

    # FIXME: create load_message to re-insert events into pipeline
    def dump_message(self, ex):
        timestamp = datetime.datetime.utcnow()
        timestamp = timestamp.isoformat()

        dump_file = "%s/%s.dump" % (self.parameters.logging_path, self.bot_id)

        new_dump_data = dict()
        new_dump_data[timestamp] = dict()
        new_dump_data[timestamp]["bot_id"] = self.bot_id
        new_dump_data[timestamp]["source_queue"] = self.source_queues
        new_dump_data[timestamp]["traceback"] = traceback.format_exc(ex)
        new_dump_data[timestamp]["message"] = self.current_message

        try:
            with open(dump_file, 'r') as fp:
                dump_data = json.load(fp)
                dump_data.update(new_dump_data)
        except:
            dump_data = new_dump_data

        with open(dump_file, 'w') as fp:
            json.dump(dump_data, fp, indent=4, sort_keys=True)

    '''
        Load Configurations
    '''

    def load_system_configuration(self):
        setattr(self.parameters, 'logging_path', DEFAULT_LOGGING_PATH)
        setattr(self.parameters, 'logging_level', DEFAULT_LOGGING_LEVEL)

        config = utils.load_configuration(SYSTEM_CONF_FILE)
        for option, value in config.iteritems():
            setattr(self.parameters, option, value)

    def load_defaults_configuration(self):

        # Load defaults configuration section

        config = utils.load_configuration(DEFAULTS_CONF_FILE)

        self.logger.debug("Defaults configuration"
                          " from '%s' file" % DEFAULTS_CONF_FILE)

        for option, value in config.iteritems():
            setattr(self.parameters, option, value)
            self.logger.debug("Defaults configuration: parameter '%s' "
                              "loaded with value '%s'" % (option, value))

    def load_runtime_configuration(self):

        # Load bot runtime configuration section

        config = utils.load_configuration(RUNTIME_CONF_FILE)

        self.logger.debug("Runtime configuration: loading '%s' section from"
                          " '%s' file" % (self.bot_id, RUNTIME_CONF_FILE))

        if self.bot_id in config.keys():
            for option, value in config[self.bot_id].iteritems():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter '%s' "
                                  "loaded with value '%s'" % (option, value))

    def load_pipeline_configuration(self):
        config = utils.load_configuration(PIPELINE_CONF_FILE)

        self.logger.debug("Pipeline configuration: loading '%s' section"
                          " from '%s' file" % (self.bot_id, PIPELINE_CONF_FILE))

        self.source_queues = None
        self.destination_queues = None

        if self.bot_id in config.keys():

            if 'source-queue' in config[self.bot_id].keys():
                self.source_queues = config[self.bot_id]['source-queue']
                self.logger.debug("Pipeline configuration: parameter "
                                  "'source-queue' loaded with the value '%s'"
                                  % self.source_queues)

            if 'destination-queues' in config[self.bot_id].keys():

                self.destination_queues = config[self.bot_id]['destination-queues']
                self.logger.debug("Pipeline configuration: parameter"
                                  "'destination-queues' loaded with the value"
                                  " '%s'" % ", ".join(self.destination_queues))

        else:
            self.logger.error("Pipeline configuration: failed to load configuration")
            self.stop()

    def load_harmonization_configuration(self):
        harmonization_config = utils.load_configuration(HARMONIZATION_CONF_FILE)
        self.logger.debug("Harmonization configuration: loading all '%s' file" %
                          HARMONIZATION_CONF_FILE)

        for message_types in harmonization_config.keys():
            for key in harmonization_config[message_types].keys():
                for _key in harmonization_config.keys():
                    if _key.startswith("%s." % key):    # FIXME: write in devguide the rules for the keys names
                        raise exceptions.ConfigurationError(
                            HARMONIZATION_CONF_FILE, "key %s is not valid" % _key)


class Parameters(object):
    pass
