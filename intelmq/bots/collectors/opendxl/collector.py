"""
openDXL Collector Bot
Connects to a openDXL fabric and subscribes to ATD topic
TLS is used by default.

Parameters:
dxl_config_file: string
dxl_topic: string
"""

import logging
import os
import sys
import time
import json
import threading
import importlib

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event, Request

from intelmq.lib.bot import CollectorBot

class openDXLCollectorBot(CollectorBot):

    dxlclient=None

    def process(self):

        if self.dxlclient==None:
            self.dxlclient=DXLClient(self.parameters.dxl_config_file, self.parameters.dxl_topic,
                                     self.new_report, self.send_message, self.logger)
            self.dxlclient.start()
            self.logger.info('DXL Client started.')

class DXLClient():

    def __init__(self, dxl_config_file, dxl_topic, 
                 object_report, object_send_message, object_logger):

        self.config = DxlClientConfig.create_dxl_config_from_file(dxl_config_file)
        self.send_message=object_send_message
        self.report=object_report
        self.logger=object_logger

    def start(self):
        with DxlClient(self.config) as self.client:

            # Connect to the fabric
            try:
                self.client.connect()
                if self.client.connected:
                    self.logger.info('DXL Client connected')
            except Exception:
                self.logger.error('Error during client connect.')
                raise

            # Create and add event listener
            class MyEventCallback(EventCallback):

                # def __init__(self,object_logger):
                #    object_logger.info("Test with self.logger")
 
                def on_event(self,event):

                    self.parse_message(event.payload.decode())

                @staticmethod
                def parse_message(object_message):
                    self.logger.debug('Received Message %r', object_message)

                    # Read msg-body and add as raw to a new report.
                    # now it's up to a parser to do the interpretation of the message.
                    try:
                        object_report=self.report()
                        object_report.add("raw", json.dumps(object_message, sort_keys=True))
                        self.send_message(object_report)
                    except Exception as err:
                        self.logger.error("Error when adding message to pipeline")


                @staticmethod
                def worker_thread(req):
                    self.client.sync_request(req)

            # Register the callback with the client
            self.client.add_event_callback('#', MyEventCallback(), subscribe_to_topic=False)
            self.client.subscribe(dxl_topic)

            # Wait forever
            while True:
                time.sleep(60)

    def stop(self):
        if self.client:
            if self.client.disconnect():
                self.logger.info("Disconnected from DXL fabric.")
            else:
                self.logger.error("Could not disconnect from DXL fabric.")
        else:
            self.logger.info("There was no openDXL client I could stop.")

if __name__ == "__main__":
    bot = openDXLCollectorBot(sys.argv[1])
    bot.start()

BOT = openDXLCollectorBot
