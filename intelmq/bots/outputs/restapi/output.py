import requests, json
from intelmq.lib.bot import Bot, sys

class RestApi(Bot):

    def init(self):
        url = self.parameters.host
        
    def process(self):
        event = self.receive_message()
        try:
            r = requests.post(self.parameters.host, event.to_json())
        except e:
            self.logger.error("Failed to send request: " + e.args[1])
        self.acknowledge_message()


if __name__ == "__main__":
    bot = RestApi(sys.argv[1])
    bot.start()

