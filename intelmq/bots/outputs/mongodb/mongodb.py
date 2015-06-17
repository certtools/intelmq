import pymongo
from intelmq.lib.bot import Bot, sys

class MongoDBBot(Bot):

    def init(self):
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
