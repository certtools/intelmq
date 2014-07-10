import re
import time
import traceback
import ConfigParser

from lib.pipeline import *
from lib.utils import *
from lib.cache import *
from lib.event import *


SYSTEM_CONF_FILE = "conf/system.conf"
PIPELINE_CONF_FILE = "conf/pipeline.conf"
BOTS_CONF_FILE = "conf/bots.conf"
LOGS_PATH = "logs/"

class Bot(object):

    def __init__(self, bot_id):
        self.check_bot_id(bot_id)

        self.bot_id = bot_id

        self.logger = self.load_logger()
        self.logger.info('Bot is starting')

        self.load_configurations()

        src_queue, dest_queues = self.load_queues()
        self.pipeline = self.load_pipeline(src_queue, dest_queues)

        self.init()


    def init(self):
        pass


    def check_bot_id(self, str):
        res = re.search('[^0-9a-zA-Z\-]+', str)
        if res:
            print "Invalid bot id."
            self.stop()


    def start(self):
         self.logger.info('Bot start processing')
 
         while True:
             try:
                self.process()
                time.sleep(int(self.parameters.processing_interval))
             except:
                # self.close() # add this method
                self.logger.info('Bot is restarting')
                self.connect() 
                self.logger.error(traceback.format_exc())                
                time.sleep(5)

    
    def stop(self):
        try:
            self.logger.error("Bot found an error. Exiting")
        except:
            pass
        finally:
            print "Bot found an error. Exiting"
        exit(-1)


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


    def load_pipeline(self, src_queue, dest_queues):
        self.logger.debug("Connecting to pipeline queues")
        return Pipeline(src_queue, dest_queues)


    def load_queues(self):
        config = ConfigParser.ConfigParser()
        config.read(PIPELINE_CONF_FILE)
        self.logger.debug("Loading pipeline queues from '%s' file" % PIPELINE_CONF_FILE)
        
        for option in config.options("Pipeline"):
            if option == self.bot_id:
                queues = config.get("Pipeline", self.bot_id)

                src_queue, dest_queues = self.parse_queues(queues)
                if src_queue or dest_queues:
                    self.logger.info("Source queue '%s'" % src_queue)
                    self.logger.info("Destination queue(s) '%s'" % dest_queues)
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
            message = Event.from_unicode(raw_message)
        except:
            message = raw_message
        return message


    def acknowledge_message(self):
        self.pipeline.acknowledge()


class Parameters(object):
    pass

