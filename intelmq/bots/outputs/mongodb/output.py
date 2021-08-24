# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
pymongo library automatically tries to reconnect if connection has been lost.
"""

import dateutil.parser

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pymongo
except ImportError:
    pymongo = None


class MongoDBOutputBot(Bot):
    """Send events to a MongoDB database"""
    collection = None
    database = None
    db_pass = None
    db_user = None
    hierarchical_output: bool = False
    host: str = "localhost"
    port: int = 27017
    replacement_char = '_'

    username = None
    password = None
    _client = None
    _collection = None

    def init(self):
        if pymongo is None:
            raise MissingDependencyError("pymongo")

        self.pymongo_3 = pymongo.version_tuple >= (3, )
        self.pymongo_35 = pymongo.version_tuple >= (3, 5)

        if self.replacement_char == '.':
            raise ValueError('replacement_char should be different than .')

        self.username = self.db_user
        self.password = self.db_pass
        if not self.password:  # checking for username is sufficient then
            self.username = None

        self.connect()

    def connect(self):
        self.logger.debug('Getting server info.')
        server_info = pymongo.MongoClient(self.host, self.port).server_info()
        server_version = server_info['version']
        server_version_split = tuple(server_version.split('.'))
        self.logger.debug('Connecting to MongoDB server version %s.',
                          server_version)
        try:
            if self.pymongo_35 and self.username and server_version_split >= ('3', '4'):
                self._client = pymongo.MongoClient(self.host,
                                                   self.port,
                                                   username=self.username,
                                                   password=self.password)
            else:
                self._client = pymongo.MongoClient(self.host,
                                                   self.port)
        except pymongo.errors.ConnectionFailure:
            raise ValueError('Connection to MongoDB server failed.')
        else:
            db = self._client[self.database]
            if self.username and not self.pymongo_35 or server_version_split < ('3', '4'):
                self.logger.debug('Trying to authenticate to database %s.',
                                  self.database)
                try:
                    db.authenticate(name=self.db_user,
                                    password=self.db_pass)
                except pymongo.errors.OperationFailure:
                    raise ValueError('Authentication to database {} failed'.format(self.database))
            self._collection = db[self.collection]
            self.logger.info('Successfully connected to MongoDB server.')

    def process(self):
        event = self.receive_message()

        if self.hierarchical_output:
            tmp_dict = event.to_dict(hierarchical=True)
            if "time" in tmp_dict:
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
            if self.pymongo_3:
                self._collection.insert_one(tmp_dict)
            else:
                self._collection.insert(tmp_dict)
        except pymongo.errors.AutoReconnect:
            self.logger.error('Connection Lost. Connecting again.')
            self.connect()
        else:
            self.acknowledge_message()

    def shutdown(self):
        if self._client:
            self._client.close()


BOT = MongoDBOutputBot
