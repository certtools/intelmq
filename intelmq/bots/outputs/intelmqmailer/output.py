# -*- coding: utf-8 -*-
import sys

import dateutil.parser

from intelmq.lib.bot import Bot

try:
    import pymongo
except ImportError:
    pymongo = None


class IntelMQMailerOutputBot(Bot):

    def init(self):
        if pymongo is None:
            self.logger.error('Could not import pymongo. Please install it.')
            self.stop()

        client = pymongo.MongoClient(self.parameters.host,
                                     int(self.parameters.port))
        db = client[self.parameters.database]
        self.collection = db[self.parameters.collection]

    def process(self):
        event = self.receive_message()

        event_dict = event.to_dict()

        time = event_dict['time']['observation']
        event_dict['time']['observation'] = dateutil.parser.parse(time)

        self.collection.insert(event_dict)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = IntelMQMailerOutputBot(sys.argv[1])
    bot.start()
