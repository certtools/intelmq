# -*- coding: utf-8 -*-
import sys

import dateutil.parser
import pymongo

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
