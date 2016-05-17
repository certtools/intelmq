# -*- coding: utf-8 -*-
import socket
import sys
import unicodedata

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class UDPBot(Bot):

    def init(self):
        self.delimiter = self.parameters.field_delimiter
        self.header = self.parameters.header
        self.udp_host = self.parameters.ip
        self.udp_port = int(self.parameters.port)
        self.upd_address = (self.udp_host, self.udp_port)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.raw_field = self.parameters.raw_field
        self.format = self.parameters.format

    def process(self):
        event = self.receive_message()

        if self.raw_field.upper() == 'DROP':
            del event['raw']

        if self.format.upper() == 'JSON':
            self.send(self.header + ' ' + event.to_json())
        else:
            self.send(self.delimited(event))

    def remove_control_char(self, s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

    def delimited(self, event):
        log_line = self.header
        for key, value in event.items():
            log_line += self.delimiter + key + ':' + str(value)

        return log_line

    def send(self, rawdata):
        data = utils.encode(self.remove_control_char(rawdata))
        try:
            self.udp.sendto(data, self.upd_address)
        except:
            self.logger.exception('Failled to sent message to {}:{} !'
                                  .format(self.udp_host, self.udp_port))
        else:
            self.acknowledge_message()


if __name__ == "__main__":
    bot = UDPBot(sys.argv[1])
    bot.start()
