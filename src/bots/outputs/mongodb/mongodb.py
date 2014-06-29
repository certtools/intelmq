import sys
import pymongo
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

class MongoDBBot(Bot):

    def __init__(self, bot_id):
        super(MongoDBBot, self).__init__(bot_id)
        client = pymongo.MongoClient(self.parameters.host, int(self.parameters.port))
        db = client[self.parameters.database]
        self.collection = db[self.parameters.collection]
        

    def process(self):
        event = self.receive_message()
        
        if event:
            self.collection.insert(event.to_dict())
        self.acknowledge_message()


if __name__ == "__main__":
    bot = MongoDBBot(sys.argv[1])
    bot.start()
