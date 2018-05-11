# -*- coding: utf-8 -*-

import socket
import struct
import sys

from intelmq.lib.bot import CollectorBot


class TCPCollectorBot(CollectorBot):

    def init(self):
        self.address = (self.parameters.ip, int(self.parameters.port))
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
        conn = None
        try:
            conn, addr = self.con.accept()
            self.logger.info('Connection address: %s.', addr)
            while True:
                # Read message length and unpack it into an integer
                raw_msglen = self.recvall(conn, 4)
                if not raw_msglen:
                    conn.send(b"OK")
                    return

                # Read the message data
                msg = self.recvall(conn, struct.unpack('>I', raw_msglen)[0])
                if not msg:
                    self.logger.warning('Incomplete message received from %s.', addr)
                    conn.send(b"Incomplete message")
                    return

                report = self.new_report()
                report.add("raw", msg)
                self.send_message(report)
        except socket.error:
            self.logger.exception("Reconnecting.")
            self.con.close()
            self.connect()
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
