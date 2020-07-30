# -*- coding: utf-8 -*-

import socket
import struct

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
            while True:
                # Read message length and unpack it into an integer
                raw_msglen = self.recvall(conn, 4)
                if not raw_msglen:
                    conn.send(b"End")
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

                if msg:  # if the partner connection ended, our message are already sent
                    conn.sendall(b"Ok")
                    pass
        except socket.error:
            self.logger.exception("Socket error.")
        finally:
            if conn:
                conn.close()

    def connect(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                            struct.pack('ii', 1, 0))  # immediately unbind port after closing so that we can restart
        self.con.bind(self.address)
        self.con.settimeout(15)
        self.con.listen()
        self.logger.info("Connected successfully to %s:%s.", self.address[0], self.address[1])

    def shutdown(self):
        self.con.close()


BOT = TCPCollectorBot
