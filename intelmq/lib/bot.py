import re
import sys
import json
import time
import ConfigParser

from intelmq.lib.message import Event
from intelmq.lib.pipeline import Pipeline
from intelmq.lib.utils import decode, log

SYSTEM_CONF_FILE = "/opt/intelmq/etc/system.conf"
PIPELINE_CONF_FILE = "/opt/intelmq/etc/pipeline.conf"
RUNTIME_CONF_FILE = "/opt/intelmq/etc/runtime.conf"
DEFAULT_LOGGING_PATH = "/opt/intelmq/var/log/"
DEFAULT_LOGGING_LEVEL = "INFO"


class Bot(object):

    def __init__(self, bot_id, parameters=None):
        self.parameters = parameters or Parameters()

        self.current_message = None
        self.last_message = None
        self.message_counter = 0

        self.check_bot_id(bot_id)
        self.bot_id = bot_id

        self.load_system_configurations()

        self.logger = log(self.parameters.logging_path,
                          self.bot_id,
                          self.parameters.logging_level)

        self.logger.info('Bot is starting')

        self.load_runtime_configurations()
        self.load_pipeline_configurations()

        self.init()

    def init(self):
        """Initializes a bot"""
        pass

    def start(self):
        """Starts a bot"""
        self.source_pipeline = None
        self.destination_pipeline = None
        local_retry_delay = 0
        self.parameters.retry_delay = 30 # Temporary fix. Need to add to BOTS conf

        self.logger.info('Bot start processing')

        while True:
            try:
                if not self.source_pipeline:
                    time.sleep(local_retry_delay)
                    self.logger.info("Connecting to source pipeline")
                    self.source_pipeline = Pipeline()
                    self.source_pipeline.source_queues(self.source_queues)
                    self.logger.info("Connected to source pipeline")

                if not self.destination_pipeline:
                    time.sleep(local_retry_delay)
                    self.logger.info("Connecting to destination pipeline")
                    self.destination_pipeline = Pipeline()
                    self.destination_pipeline.destination_queues(self.destination_queues)
                    self.logger.info("Connected to destination pipeline")

                self.process()
                self.logger.info("Bot stops processing. Sleeps for 'rate_limit' = %ds" % self.parameters.rate_limit)
                self.source_pipeline.sleep(self.parameters.rate_limit)

            except Exception as ex:
                local_retry_delay = self.parameters.retry_delay
                self.logger.info("Last Correct Message(event): %r" % self.last_message)
                self.logger.info("Current Message(event): %r" % self.current_message)
                self.logger.exception("Check the following exception:")
                self.logger.error('Pipeline connection failed (%r)' % ex)
                self.logger.info('Pipeline will reconnect in %s seconds' % local_retry_delay)
                self.source_pipeline = None
                self.destination_pipeline = None

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
        """Stops a bot"""
        try:
            self.logger.error("Bot found an error. Exiting")
        except:
            pass
        finally:
            print "Bot found an error. Exiting"
        exit(-1)

    def check_bot_id(self, str):
        """Returns True if the given str is a valid bot id"""
        res = re.search('[^0-9a-zA-Z\-]+', str)
        if res:
            print "Invalid bot id."
            self.stop()

    def load_config_file(self, path):
        """Loads the given json config file and returns it parsed"""
        with open(path, 'r') as fpconfig:
            config = json.loads(fpconfig.read())
        
        return config

    def load_system_configurations(self, path=SYSTEM_CONF_FILE):
        """Instructs a bot to load the system configuration (json)"""

        self.process_system_configuration(self.load_config_file(path))

    def load_runtime_configurations(self, path=RUNTIME_CONF_FILE):
        """Load runtime json configuration for a bot from given path or from default location if empty"""

        self.logger.debug("Runtime configuration: loading sections from '%s' file" % path)
        self.process_runtime_configuration(self.load_config_file(path))

    def load_pipeline_configurations(self, path=PIPELINE_CONF_FILE):
        """Load pipeline json configuration file"""

        self.logger.debug("Pipeline configuration: loading '%s' section from '%s' file" % (self.bot_id, path))

        self.source_queues = None
        self.destination_queues = None

        self.process_pipeline_configuration(self.load_config_file(path))

    def process_system_configuration(self, config):
        """Processes the loaded system configuration in config 
           and sets bot attributes accordingly"""

        setattr(self.parameters, 'logging_path', DEFAULT_LOGGING_PATH)
        setattr(self.parameters, 'logging_level', DEFAULT_LOGGING_LEVEL)

        for option, value in config.iteritems():
            setattr(self.parameters, option, value)

    def process_runtime_configuration(self, config):
        """Processes the loaded configuration keys in config and 
            sets bot attributes accordingly"""

        # Load __default__ runtime configuration section

        self.logger.debug("Runtime configuration: loading '%s' section" % "__default__")
        if "__default__" in config.keys():
            for option, value in config["__default__"].iteritems():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter '%s' loaded with the value '%s'" % (option, value))

        # Load bot runtime configuration section

        self.logger.debug("Runtime configuration: loading '%s' section" % self.bot_id)
        if self.bot_id in config.keys():
            for option, value in config[self.bot_id].iteritems():
                setattr(self.parameters, option, value)
                self.logger.debug("Runtime configuration: parameter '%s' loaded with the value '%s'" % (option, value))

    def process_pipeline_configuration(self, config):
        """Processes the loaded pipeline configuration keys in config and
            sets bot attributes accordingly"""

        if self.bot_id in config.keys():

            if 'source-queue' in config[self.bot_id].keys():
                self.source_queues = config[self.bot_id]['source-queue']
                self.logger.debug("Pipeline configuration: parameter 'source-queue' loaded with the value '%s'" % self.source_queues)

            if 'destination-queues' in config[self.bot_id].keys():
                self.destination_queues = config[self.bot_id]['destination-queues']
                self.logger.debug("Pipeline configuration: parameter 'destination-queues' loaded with the value '%s'" % ", ".join(self.destination_queues))

        else:
            self.logger.error("Pipeline configuration: failed to load configuration")
            self.stop()

    def send_message(self, message):
        """Sends a given message with configured destination pipeline"""

        if not message:
            self.logger.warning("Empty message found.")
            return False

        if isinstance(message, Event):
            message = unicode(message)  # convert Event Object to string (UTF-8)

        self.message_counter += 1
        if self.message_counter % 500 == 0:
            self.logger.info("Processed %s messages" % self.message_counter)

        self.destination_pipeline.send(message)

    def receive_message(self):
        """Receive a message from the configured source queue"""
        self.current_message = self.source_pipeline.receive()

        if not self.current_message:
            return None

        message = self.current_message.decode('utf-8')

        try:     # Event Object
            return Event.from_unicode(message)
        except:  # Report Object
            return message

    def acknowledge_message(self):
        """Acknowledge a message and remove it from the queue system permanently"""
        self.last_message = self.current_message
        self.source_pipeline.acknowledge()


class Parameters(object):
    pass
