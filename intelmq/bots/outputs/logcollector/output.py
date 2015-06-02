import time
import socket
from intelmq.lib.bot import Bot, sys

class LogCollectorBot(Bot):

    def process(self):       
        event = self.receive_message()
        data = event.to_json()
        self.send_data(data)
        self.acknowledge_message()


    def connect(self):
        address = (self.parameters.ip, int(self.parameters.port))
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                self.con.connect(address)
                break
            except socket.error, e:
                self.logger.error(e.args[1] + ". Retrying in 10 seconds.")
                time.sleep(10)

        self.logger.info("Connected successfully to %s:%i", address[0], address[1])

        
    def send_data(self, data):
        while True:
            try:
                self.con.send(unicode(data).encode("utf-8"))
                self.con.sendall("")
                break
            except socket.error, e:
                self.logger.error(e.args[1] + ". Reconnecting..")
                self.con.close()
                self.connect()
            except AttributeError:
                self.connect()


if __name__ == "__main__":
    bot = LogCollectorBot(sys.argv[1])
    bot.start()
