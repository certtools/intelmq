# -*- coding: utf-8 -*-
"""Import Syslog messages

SPDX-FileCopyrightText: 2020 Linköping University <https://liu.se/>
SPDX-License-Identifier: AGPL-3.0-or-later

One IntelMQ event per Syslog line. Multi-line Syslog messages are not
supported.

Parameters:

    ip: string, optional, bind IP (or wildcard, if not set)

    name: string, optional, feed name, default "Syslog"

    port: integer, optional, listen port, default 514

    protocol: string, optional, default "udp". Only UDP is implemented
              currently.

    provider: string, optional, feed provider name, default "Syslog"

"""

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import ConfigurationError

import socketserver


class SyslogCollectorBot(CollectorBot):

    def init(self):
        self.ip = getattr(self.parameters, 'ip', '0.0.0.0')
        self.name = getattr(self.parameters, 'name', 'Syslog')
        self.port = int(getattr(self.parameters, 'port', 514))
        self.protocol = getattr(self.parameters, 'protocol', 'udp').lower()
        if self.protocol not in ['udp']:
            raise ConfigurationError('Listen port',
                                     'Invalid protocol %s' % self.protocol)
        self.provider = getattr(self.parameters, 'provider', 'Syslog')

        if self.protocol == 'udp':
            self.server = socketserver.UDPServer((self.ip, self.port), SyslogUDP)
        self.server.logger = self.logger
        self.server.send_message = self.send_message
        self.server.new_report = self.new_report
        self.logger.info("Listening on %s:%d/%s",
                         self.ip, self.port, self.protocol)

    def process(self):
        self.server.serve_forever()


class SyslogUDP(socketserver.BaseRequestHandler):
    def handle(self):
        line = self.request[0].strip()
        self.server.logger.debug("Received event from %s", self.client_address)
        report = self.server.new_report()
        report.add('raw', line)
        self.server.send_message(report)
        self.finish()


BOT = SyslogCollectorBot
