# -*- coding: utf-8 -*-
"""
For intelmq collectors on the other side we can expect the "ok" sent back.
Otherwise, for filebeat and other we can't do that.
As this was the previous behavior, that's the default.
https://github.com/certtools/intelmq/issues/1385
"""
import socket
import struct
import time

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class TCPOutputBot(Bot):

    is_multithreadable = False

    def init(self):
        self.to_intelmq = getattr(self.parameters, "counterpart_is_intelmq", False)

        self.address = (self.parameters.ip, int(self.parameters.port))
        self.separator = utils.encode(self.parameters.separator) if (hasattr(self.parameters, "separator")) else None
        self.connect()

    def recvall(self, conn, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def process(self):
        event = self.receive_message()

        data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        try:
            while True:
                if self.separator:
                    self.con.sendall(utils.encode(data) + self.separator)
                else:
                    d = utils.encode(data)
                    msg = struct.pack('>I', len(d)) + d
                    self.con.sendall(msg)
                if self.to_intelmq:
                    response = self.con.recv(2)
                    if response == b"Ok":
                        break
                    self.logger.warn("Message not delivered, retrying.")
                    time.sleep(1)
                else:
                    break
        except socket.error as e:
            self.logger.exception("Reconnecting, %s", e)
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
        self.con.settimeout(15)
        self.logger.info("Connected successfully to %s:%s.",
                         self.address[0], self.address[1])


BOT = TCPOutputBot
