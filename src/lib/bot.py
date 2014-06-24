import time
import traceback
import ConfigParser

from lib.pipeline import *
from lib.utils import *
from lib.cache import *


SYSTEM_CONF_FILE = "conf/system.conf"
PIPELINE_CONF_FILE = "conf/pipeline.conf"
BOTS_CONF_FILE = "conf/bots.conf"


class Bot(object):

    def __init__(self, name):
        self.name = name
        self.logger = self.get_logger()
        self.logger.info('Bot is starting')

        self.get_bot_configurations()

        src_queue, dest_queue = self.get_queues()
        self.pipeline = self.get_pipeline(src_queue, dest_queue)

        if self.parameters.cached:
            cache_db_index = 10 #FIXME
            self.cache = self.create_cache(cache_db_index, self.parameters.cache_ttl)


    def get_bot_configurations(self):
        self.parameters = Parameters()
        config = ConfigParser.ConfigParser()
        config.read(BOTS_CONF_FILE)
        
        default_section = "default"
        self.logger.debug("Loading configuration in default section from '%s' file" % BOTS_CONF_FILE)
        
        if config.has_section(default_section):
            for option in config.options(default_section):
                setattr(self.parameters, option, config.get(default_section, option))
                self.logger.debug("Parameter '%s' loaded with the value '%s'" % (option, config.get(default_section, option)))
        
        self.logger.debug("Loading configuration in %s section from '%s' file" % (self.name, BOTS_CONF_FILE))
        
        if config.has_section(self.name):
            for option in config.options(self.name):
                setattr(self.parameters, option, config.get(self.name, option))
                self.logger.debug("Parameter '%s' loaded with the value '%s'" % (option, config.get(self.name, option)))


    def get_logger(self):
        config = ConfigParser.ConfigParser()
        config.read(SYSTEM_CONF_FILE)
        loglevel = config.get('Logging','level')
        return log(self.name, loglevel)


    def create_cache(self, cache_id, ttl):
        config = ConfigParser.ConfigParser()
        config.read(SYSTEM_CONF_FILE)

        host = config.get('Redis', 'host')
        port = int(config.get('Redis', 'port'))
        self.logger.debug("Connecting to Redis cache '%s:%s'" % (host, port))
        return Cache(host, port, cache_id, ttl)


    def get_pipeline(self, src_queue, dest_queue):
        self.logger.debug("Connecting to pipeline queues")
        return Pipeline(src_queue, dest_queue)


    def get_queues(self):
        config = ConfigParser.ConfigParser()
        config.read(PIPELINE_CONF_FILE)
        self.logger.debug("Loading pipeline queues from '%s' file" % PIPELINE_CONF_FILE)
        
        for option in config.options("Pipeline"):
            if option == self.name:
                queues = config.get("Pipeline", self.name)
                queues = queues.split('|')
                
                if len(queues) == 2:
                    src_queue = queues[0].strip()
                    dest_queue = queues[1].strip()
                    
                    if src_queue == "None":
                        src_queue = None
                    if dest_queue == "None":
                        dest_queue = None
                    
                    self.logger.info("Source queue '%s'" % src_queue)
                    self.logger.info("Destination queue '%s'" % dest_queue)
                    
                    return [src_queue, dest_queue]
        
        self.logger.error("Failed to load queues")
        self.exit()
            

    def start(self):
        self.logger.info('Bot start processing')

        while True:
            try:
                self.process()
                time.sleep(int(self.parameters.processing_interval))
            except:
                self.logger.error(traceback.format_exc())
                self.exit()
    
    def exit(self):
        self.logger.error("Bot found an error. Exiting")
        exit(-1)


class Parameters(object):
    pass

