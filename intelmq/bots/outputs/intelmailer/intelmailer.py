import datetime, pymongo
from intelmq.lib.bot import Bot, sys

class IntelMailerBot(Bot):

    def init(self):
        client = pymongo.MongoClient(self.parameters.host, int(self.parameters.port))
        db = client[self.parameters.database]
        self.collection = db[self.parameters.collection]
       

    def process(self):
        event = self.receive_message()
        
        if event:
            event_dict = event.to_dict()
            event_dict['created_at'] = datetime.datetime.utcnow()
            self.collection.insert(event_dict)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = IntelMailerBot(sys.argv[1])
    bot.start()
