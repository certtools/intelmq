# -*- coding: utf-8 -*-
"""
pymongo library automatically tries to reconnect if connection has been lost
"""

from intelmq.lib.bot import Bot
import dateutil.parser

try:
    import pymongo
except ImportError:
    pymongo = None


class MongoDBOutputBot(Bot):

    def init(self):
        if pymongo is None:
            raise ValueError('Could not import pymongo. Please install it.')

        self.connect()

    def connect(self):
        self.logger.debug('Connecting to MongoDB server.')
        try:
            self.client = pymongo.MongoClient(self.parameters.host,
                                              int(self.parameters.port))
        except pymongo.errors.ConnectionFailure:
            raise ValueError('Connection to MongoDB server failed.')
        else:
            db = self.client[self.parameters.database]
            if hasattr(self.parameters, 'db_user') and hasattr(self.parameters, 'db_pass'):
                self.logger.debug('Trying to authenticate to database %s.',
                                  self.parameters.database)
                try:
                    db.authenticate(name=self.parameters.db_user,
                                    password=self.parameters.db_pass)
                except pymongo.errors.OperationFailure:
                    raise ValueError('Authentication to database {} failed'.format(self.parameters.database))
            self.collection = db[self.parameters.collection]
            self.logger.info('Successfully connected to MongoDB server.')

    def process(self):
        event = self.receive_message()

        try:
            tmp_dict = event.to_dict(hierarchical=self.parameters.hierarchical_output)
            tmp_dict["time"]["observation"] = dateutil.parser.parse(tmp_dict["time"]["observation"])
            tmp_dict["time"]["source"] = dateutil.parser.parse(tmp_dict["time"]["source"])
            self.collection.insert(tmp_dict)
        except pymongo.errors.AutoReconnect:
            self.logger.error('Connection Lost. Connecting again.')
            self.connect()
        else:
            self.acknowledge_message()

    def shutdown(self):
        self.client.close()


BOT = MongoDBOutputBot
