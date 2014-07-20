import sys
import re
import time
import ConfigParser

from intelmq.lib.event import Event
from intelmq.lib.pipeline import Pipeline
from intelmq.lib.utils import force_decode, log


SYSTEM_CONF_FILE = "/etc/intelmq/system.conf"
PIPELINE_CONF_FILE = "/etc/intelmq/pipeline.conf"
BOTS_CONF_FILE = "/etc/intelmq/bots.conf"
LOGS_PATH = "/var/log/intelmq/"


class Bot(object):

    def __init__(self, bot_id):
        self.check_bot_id(bot_id)

        self.bot_id = bot_id

        self.logger = self.load_logger()
        self.logger.info('Bot is starting')

        self.load_configurations()

        self.src_queue, self.dest_queues = self.load_queues()
        self.parameters.processing_interval = float(self.parameters.processing_interval)
        
        self.init()


    def init(self):
        pass


    def start(self):
        self.logger.info('Bot start processing')
        self.pipeline = None
 
        while True:
            try:
                if not self.pipeline:
                    self.logger.info("Connecting to pipeline queues")
                    self.pipeline = Pipeline(self.src_queue, self.dest_queues)
                    self.logger.info("Connected to pipeline queues. Start processing.")
                self.process()
                self.pipeline.sleep(self.parameters.processing_interval)
                
            except Exception as e:
                retry_delay = 30
                self.logger.error('Pipeline connection failed (%s)' % e)
                self.logger.info('Pipeline will reconnect in %s seconds' % retry_delay)
                time.sleep(retry_delay)
                self.pipeline = None
                
            except KeyboardInterrupt as e:
                if self.pipeline:
                    self.pipeline.disconnect()
                    self.logger.info("Disconnecting from pipeline")
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


    def load_configurations(self):
        self.parameters = Parameters()
        config = ConfigParser.ConfigParser()
        config.read(BOTS_CONF_FILE)
        
        default_section = "default"
        self.logger.debug("Loading configuration in default section from '%s' file" % BOTS_CONF_FILE)
        
        if config.has_section(default_section):
            for option in config.options(default_section):
                setattr(self.parameters, option, config.get(default_section, option))
                self.logger.debug("Parameter '%s' loaded with the value '%s'" % (option, config.get(default_section, option)))
        
        self.logger.debug("Loading configuration in %s section from '%s' file" % (self.bot_id, BOTS_CONF_FILE))
        
        if config.has_section(self.bot_id):
            for option in config.options(self.bot_id):
                setattr(self.parameters, option, config.get(self.bot_id, option))
                self.logger.debug("Parameter '%s' loaded with the value '%s'" % (option, config.get(self.bot_id, option)))


    def load_logger(self):
        config = ConfigParser.ConfigParser()
        config.read(SYSTEM_CONF_FILE)
        loglevel = config.get('Logging','level')
        return log(LOGS_PATH, self.bot_id, loglevel)


    def load_pipeline(self):
        return


    def load_queues(self):
        config = ConfigParser.ConfigParser()
        config.read(PIPELINE_CONF_FILE)
        self.logger.debug("Loading pipeline queues from '%s' file" % PIPELINE_CONF_FILE)
        
        for option in config.options("Pipeline"):
            if option == self.bot_id:
                queues = config.get("Pipeline", self.bot_id)

                src_queue, dest_queues = self.parse_queues(queues)
                if src_queue:
                    self.logger.info("Source queue '%s'" % src_queue)
                if dest_queues:
                    self.logger.info("Destination queue(s) '%s'" % "', '".join(dest_queues))
                return [src_queue, dest_queues]

        self.logger.error("Failed to load queues")
        self.stop()
    
    
    def parse_queues(self, queues):
        queues = queues.split('|')
        
        if len(queues) == 2:
            src_queue = queues[0].strip()
            if len(src_queue) == 0:
                src_queue = None

            dest_queues = queues[1].strip()
            if len(dest_queues) == 0:
                dest_queues_list = None
            else:
                dest_queues_list = list()
                for queue in dest_queues.split(','):
                    dest_queues_list.append(queue.strip())

            return [src_queue, dest_queues_list]
        else:
            return [None, None]


    def send_message(self, message):
        try:
            message = unicode(message)
        except:
            message = force_decode(message)
        self.pipeline.send(message)


    def receive_message(self):
        raw_message = self.pipeline.receive()
        try:
            raw_message = force_decode(raw_message)
            message = Event.from_unicode(raw_message)
        except:
            message = raw_message
        return message


    def acknowledge_message(self):
        self.pipeline.acknowledge()


class Parameters(object):
    pass

