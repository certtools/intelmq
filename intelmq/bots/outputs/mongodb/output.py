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
        self.replacement_char = getattr(self.parameters, 'replacement_char', '_')
        if self.replacement_char == '.':
            raise ValueError('replacement_char should be different than .')
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

        if self.parameters.hierarchical_output:
            tmp_dict = event.to_dict(hierarchical=True)
            if "time"in tmp_dict:
                if "observation" in tmp_dict["time"]:
                    tmp_dict["time"]["observation"] = dateutil.parser.parse(tmp_dict["time"]["observation"])
                if "source" in tmp_dict["time"]:
                    tmp_dict["time"]["source"] = dateutil.parser.parse(tmp_dict["time"]["source"])
        else:
            # flat version
            # replace . in key by replacement_char
            tmp_dict = {key.replace('.', self.replacement_char): value for key, value in event.to_dict().items()}
            time_obs = "time%sobservation" % self.replacement_char
            if time_obs in tmp_dict:
                tmp_dict[time_obs] = dateutil.parser.parse(tmp_dict[time_obs])
            time_src = "time%source" % self.replacement_char
            if time_src in tmp_dict:
                tmp_dict[time_src] = dateutil.parser.parse(tmp_dict[time_obs])

        try:
            self.collection.insert(tmp_dict)
        except pymongo.errors.AutoReconnect:
            self.logger.error('Connection Lost. Connecting again.')
            self.connect()
        else:
            self.acknowledge_message()

    def shutdown(self):
        self.client.close()


BOT = MongoDBOutputBot
