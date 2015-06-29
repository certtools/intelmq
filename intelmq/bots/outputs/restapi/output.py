import requests
from intelmq.lib.bot import Bot, sys

class RestApi(Bot):


    def init(self):
        self.session = requests.Session()
#        self.session.headers.update({'X-sinkit-token': '3c5e933f0dcfb53e69fed19a88ff61a3921e0142'})
        if self.parameters.auth_token_name and self.parameters.auth_token:
            self.session.headers.update({self.parameters.auth_token_name : self.parameters.auth_token})
        
    def process(self):
        event = self.receive_message()
        try:
            r = self.session.post(self.parameters.host, event.to_json())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error("Request exception: " + str(e))
        self.acknowledge_message()


if __name__ == "__main__":
    bot = RestApi(sys.argv[1])
    bot.start()

