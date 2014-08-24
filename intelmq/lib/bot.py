import re
import sys
import json
import time
import ConfigParser

from intelmq.lib.event import Event
from intelmq.lib.pipeline import Pipeline
from intelmq.lib.utils import decode, log


SYSTEM_CONF_FILE = "/etc/intelmq/system.conf"
PIPELINE_CONF_FILE = "/etc/intelmq/pipeline.conf"
BOTS_CONF_FILE = "/etc/intelmq/runtime.conf"
LOGS_PATH = "/var/log/intelmq/"


class Bot(object):

    def __init__(self, bot_id):
        self.current_message = None
        self.last_message = None
        self.message_counter = 0

        self.check_bot_id(bot_id)

        self.bot_id = bot_id

        self.logger = self.load_logger()
        self.logger.info('Bot is starting')

        self.load_configurations()

        self.src_queue, self.dest_queues = self.load_pipeline()
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
                    self.logger.info("Connected to pipeline queues. Start processing")
                self.process()
                self.pipeline.sleep(self.parameters.processing_interval)
                
            except Exception, ex:
                retry_delay = 30
                self.logger.error("Last Correct Message(event): %r" % self.last_message)
                self.logger.error("Current Message(event): %r" % self.current_message)
                self.logger.exception("Check the following exception:")
                self.logger.error('Pipeline connection failed (%r)' % ex)
                self.logger.info('Pipeline will reconnect in %s seconds' % retry_delay)
                time.sleep(retry_delay)
                #self.pipeline.disconnect() # caused problems
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

        with open(BOTS_CONF_FILE, 'r') as fpconfig:
            config = json.loads(fpconfig.read())
        
        self.logger.debug("Loading configuration in %s section from '%s' file" % (self.bot_id, BOTS_CONF_FILE))
        
        if self.bot_id in config.keys():
            for option, value in config[self.bot_id].iteritems():
                setattr(self.parameters, option, value)
                self.logger.debug("Parameter '%s' loaded with the value '%s'" % (option, value))


    def load_logger(self):
        with open(SYSTEM_CONF_FILE, 'r') as fpconfig:
            config = json.loads(fpconfig.read())

        loglevel = config['logging_level']
        return log(LOGS_PATH, self.bot_id, loglevel)


    def load_pipeline(self):
        with open(PIPELINE_CONF_FILE, 'r') as fpconfig:
            config = json.loads(fpconfig.read())
            
        self.logger.debug("Loading pipeline queues from '%s' file" % PIPELINE_CONF_FILE)
        
        source_queue = None
        destination_queues = None
        
        if self.bot_id in config.keys():
        
            if 'source-queue' in config[self.bot_id].keys():
                source_queue = config[self.bot_id]['source-queue']
                self.logger.info("Source queue '%s'" % source_queue)
            
            if 'destination-queues' in config[self.bot_id].keys():
                destination_queues = config[self.bot_id]['destination-queues']
                self.logger.info("Destination queues '%s'" % ", ".join(destination_queues))

            return [source_queue, destination_queues]

        self.logger.error("Failed to load queues")
        self.stop()
        

    def send_message(self, message):
        if not message:
            self.logger.warning("Empty message found.")
            return False
        
        if isinstance(message, Event):
            message = unicode(message) # convert Event Object to string (UTF-8)
            
        self.message_counter += 1
        if self.message_counter % 500 == 0:
            self.logger.info("Processed %s messages" % self.message_counter)
            
        self.pipeline.send(message)


    def receive_message(self):
        self.current_message = self.pipeline.receive()
        
        if not self.current_message:
            return None
        
        message = self.current_message.decode('utf-8')
        
        try:    # Event Object
            return Event.from_unicode(message)
        
        except: # Report Object
            return message


    def acknowledge_message(self):
        self.last_message = self.current_message
        self.pipeline.acknowledge()


class Parameters(object):
    pass
