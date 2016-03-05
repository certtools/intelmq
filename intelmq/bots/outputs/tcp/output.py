# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
import sys
import time

from intelmq.lib.bot import Bot
import intelmq.lib.utils as utils


class TCPBot(Bot):

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

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
            except socket.error as exc:
                self.logger.error(exc.args[1] + ". Retrying in 10 seconds.")
                time.sleep(10)

        self.logger.info("Connected successfully to {!s}: {}"
                         "".format(address[0], address[1]))

    def send_data(self, data):
        while True:
            try:
                self.con.send(utils.encode(data))
                self.con.sendall(b"")
                break
            except socket.error as exc:
                self.logger.error(exc.args[1] + ". Reconnecting..")
                self.con.close()
                self.connect()
            except AttributeError:
                self.connect()


if __name__ == "__main__":
    bot = TCPBot(sys.argv[1])
    bot.start()
