# -*- coding: utf-8 -*-

import socket

import intelmq.lib.utils as utils
from intelmq.lib.bot import CollectorBot
from intelmq.lib.message import Event


class TCPCollectorBot(CollectorBot):

    def init(self):
        self.address = (self.parameters.ip, int(self.parameters.port))
        self.separator = utils.encode(self.parameters.separator)
        self.BUFFER_SIZE = 1024
        self.connect()

    def process(self):
        try:
            conn, addr = self.con.accept()
            print('Connection address:', addr)
            data = b""
            while True:
                b = conn.recv(self.BUFFER_SIZE)
                if not b: break

                data += b
                messages = data.split(self.separator)
                if len(messages) > 1:
                    self.logger.debug('Received parsable data: %s.', data)
                    for event in messages:
                        if event:
                            event = Event(Event.unserialize(utils.decode(event)))
                            # can't use direct self.send_message because that wants to overwrite feed.name and feed.accuracy
                            super(CollectorBot, self).send_message(event)
                    data = messages[-1]  # return back the non-finished message
            conn.send(b"OK")
        except socket.error as e:
                self.logger.exception("Reconnecting.")
                self.con.close()
                self.connect()
        except AttributeError as e:
            self.logger.info('Reconnecting.')
            self.connect()
        finally:
            if conn:
                conn.close()

    def connect(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.bind(self.address)
        self.con.listen()
        self.logger.info("Connected successfully to %s:%s.", self.address[0], self.address[1])


BOT = TCPCollectorBot
