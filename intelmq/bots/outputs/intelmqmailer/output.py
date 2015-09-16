# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import pymongo
import dateutil.parser

from intelmq.lib.bot import Bot


class IntelMQMailerOutputBot(Bot):

    def init(self):
        client = pymongo.MongoClient(self.parameters.host,
                                     int(self.parameters.port))
        db = client[self.parameters.database]
        self.collection = db[self.parameters.collection]

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        event_dict = event.to_dict()

        time = event_dict['time']['observation']
        event_dict['time']['observation'] = dateutil.parser.parse(time)

        self.collection.insert(event_dict)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = IntelMQMailerOutputBot(sys.argv[1])
    bot.start()
