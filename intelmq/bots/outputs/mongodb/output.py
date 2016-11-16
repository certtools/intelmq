# -*- coding: utf-8 -*-
"""
pymongo library automatically tries to reconnect if connection has been lost
"""
import sys

from intelmq.lib.bot import Bot

try:
    import pymongo
except ImportError:
    pymongo = None


class MongoDBOutputBot(Bot):

    def init(self):
        if pymongo is None:
            self.logger.error('Could not import pymongo. Please install it.')
            self.stop()

        self.connect()

    def connect(self):
        self.logger.debug('Connecting to mongodb server.')
        try:
            self.client = pymongo.MongoClient(self.parameters.host,
                                              int(self.parameters.port))
        except pymongo.errors.ConnectionFailure:
            raise ValueError('Connection to mongodb server failed.')
        else:
            db = self.client[self.parameters.database]
            self.collection = db[self.parameters.collection]
            self.logger.info('Successfully connected to mongodb server.')

    def process(self):
        event = self.receive_message()

        try:
            self.collection.insert(event.to_dict(hierarchical=self.parameters.hierarchical_output))
        except pymongo.errors.AutoReconnect:
            self.logger.error('Connection Lost. Connecting again.')
            self.connect()
        else:
            self.acknowledge_message()

    def shutdown(self):
        self.client.close()


if __name__ == "__main__":
    bot = MongoDBOutputBot(sys.argv[1])
    bot.start()
