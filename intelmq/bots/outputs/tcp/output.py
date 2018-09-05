# -*- coding: utf-8 -*-
import socket
import struct

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class TCPOutputBot(Bot):

    def init(self):
        self.address = (self.parameters.ip, int(self.parameters.port))
        self.separator = utils.encode(self.parameters.separator) if(hasattr(self.parameters, "separator")) else None
        self.connect()

    def process(self):
        # self.logger.exception("EDCVARD TEST.")
        event = self.receive_message()

        data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        try:
            if self.separator:
                self.con.sendall(utils.encode(data) + self.separator)
            else:
                d = utils.encode(data)
                msg = struct.pack('>I', len(d)) + d
                self.con.sendall(msg)
        except socket.error:
            # self.logger.exception("Reconnecting.")
            self.logger.info("Reconnecting!")
            self.con.close()
            self.connect()
        except AttributeError:
            self.logger.info('Reconnecting.')
            self.connect()
        else:
            self.acknowledge_message()

    def connect(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect(self.address)
        self.logger.info("Connected successfully to %s:%s.",
                         self.address[0], self.address[1])


BOT = TCPOutputBot
