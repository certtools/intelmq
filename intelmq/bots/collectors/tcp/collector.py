# -*- coding: utf-8 -*-

import socket
import sys

import intelmq.lib.utils as utils
from intelmq.lib.bot import CollectorBot


class TCPCollectorBot(CollectorBot):

    def init(self):
        self.address = (self.parameters.ip, int(self.parameters.port))
        self.separator = utils.encode(self.parameters.separator)
        self.BUFFER_SIZE = 1024
        self.connect()

    def process(self):
        conn = None
        try:
            conn, addr = self.con.accept()
            print('Connection address:', addr)
            data = b""
            while True:
                b = conn.recv(self.BUFFER_SIZE)
                if not b:
                    break

                data += b
                messages = data.split(self.separator)
                if len(messages) > 1:
                    self.logger.debug('Received parsable data: %s.', data)
                    for event in messages:
                        if event:
                            report = self.new_report()
                            report.add("raw", event)
                            self.send_message(report)
                    data = messages[-1]  # return back the non-finished message
            conn.send(b"OK")
        except socket.error as e:
            self.logger.exception("Reconnecting.")
            self.con.close()
            self.connect()
        except AttributeError as e:
            self.logger.info('Attribute error.')
        finally:
            if conn:
                conn.close()

    def connect(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.bind(self.address)
        if sys.version_info[1] > 4:  # remove when we're having Python 3.5+
            self.con.listen()
        else:
            self.con.listen(1)
        self.logger.info("Connected successfully to %s:%s.", self.address[0], self.address[1])

    def shutdown(self):
        self.con.close()


BOT = TCPCollectorBot
