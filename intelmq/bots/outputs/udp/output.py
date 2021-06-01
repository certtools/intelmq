# SPDX-FileCopyrightText: 2016 pedromreis
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import socket
import unicodedata

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class UDPOutputBot(Bot):
    """Send events to a UDP server, e.g. a syslog daemon"""
    field_delimiter: str = "|"
    format: str = None
    header: str = "<header text>"
    keep_raw_field: bool = False
    udp_host: str = "localhost"
    udp_port: int = None

    __is_multithreadable = False

    def init(self):
        self.delimiter = self.field_delimiter
        self.udp_host = socket.gethostbyname(self.udp_host)
        self.upd_address = (self.udp_host, self.udp_port)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.format = self.format.lower()
        if self.format not in ['json', 'delimited']:
            raise ValueError('Unknown format %r given. Check your configuration.' % self.format)

    def process(self):
        event = self.receive_message()

        if not self.keep_raw_field:
            del event['raw']

        if self.format == 'json':
            self.send(self.header + event.to_json())
        elif self.format == 'delimited':
            self.send(self.delimited(event))

    def remove_control_char(self, s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

    def delimited(self, event):
        log_line = self.header
        for key, value in event.items():
            log_line += self.delimiter + key + ':' + str(value)

        return log_line

    def send(self, rawdata):
        data = utils.encode(self.remove_control_char(rawdata) + '\n')
        try:
            self.udp.sendto(data, self.upd_address)
        except Exception:
            self.logger.exception('Failed to send message to %s:%s!',
                                  self.udp_host, self.udp_port)
        else:
            self.acknowledge_message()


BOT = UDPOutputBot
