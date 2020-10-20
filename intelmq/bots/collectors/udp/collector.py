# -*- coding: utf-8 -*-
"""Receive UDP messages

SPDX-FileCopyrightText: 2020 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

Creates one IntelMQ event per UDP packet.

Parameters:

    ip: string, optional, bind IP (or wildcard, if not set)

    name: string, optional, feed name, default "UDP"

    port: integer, listen port

    provider: string, optional, feed provider name, default "UDP"

"""

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import ConfigurationError

import socketserver


class UDPCollectorBot(CollectorBot):

    def init(self):
        self.ip = getattr(self.parameters, 'ip', '0.0.0.0')
        self.name = getattr(self.parameters, 'name', 'UDP')
        self.port = int(getattr(self.parameters, 'port', 0))
        if self.port == 0:
            raise ConfigurationError('Listen port',
                                     'No port specified')
        self.provider = getattr(self.parameters, 'provider', 'UDP')

        self.server = socketserver.UDPServer((self.ip, self.port), UDPServer)
        self.server.logger = self.logger
        self.server.send_message = self.send_message
        self.server.new_report = self.new_report
        self.logger.info("Listening on %s:%d/%s",
                         self.ip, self.port, self.protocol)

    def process(self):
        self.server.serve_forever()


class UDPServer(socketserver.BaseRequestHandler):
    def handle(self):
        line = self.request[0].strip()
        self.server.logger.debug("Received event from %s", self.client_address)
        report = self.server.new_report()
        report.add('raw', line)
        self.server.send_message(report)
        self.finish()


BOT = UDPServer
