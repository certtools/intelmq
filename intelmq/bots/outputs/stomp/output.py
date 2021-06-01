# SPDX-FileCopyrightText: 2016 Mauro Silva
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os.path

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError


try:
    import stomp
except ImportError:
    stomp = None


class StompOutputBot(OutputBot):
    """Send events to a STMOP server"""
    """ main class for the STOMP protocol output bot """
    exchange: str = "/exchange/_push"
    heartbeat: int = 60000
    http_verify_cert = True
    keep_raw_field: bool = False
    message_hierarchical_output: bool = False
    message_jsondict_as_string: bool = False
    message_with_type: bool = False
    port: int = 61614
    server: str = "127.0.0.1"  # TODO: could be ip address
    single_key: bool = False
    ssl_ca_certificate: str = 'ca.pem'  # TODO: could be pathlib.Path
    ssl_client_certificate: str = 'client.pem'  # TODO: pathlib.Path
    ssl_client_certificate_key: str = 'client.key'  # TODO: patlib.Path

    _conn = None

    def init(self):
        if stomp is None:
            raise MissingDependencyError("stomp")

        # check if certificates exist
        for f in [self.ssl_ca_cert, self.ssl_cl_cert, self.ssl_cl_cert_key]:
            if not os.path.isfile(f):
                raise ValueError("Could not open SSL (certificate) file '%s'." % f)

        _host = [(self.server, self.port)]
        self._conn = stomp.Connection(host_and_ports=_host, use_ssl=True,
                                      ssl_key_file=self.ssl_cl_cert_key,
                                      ssl_cert_file=self.ssl_cl_cert,
                                      ssl_ca_certs=self.ssl_ca_cert,
                                      heartbeats=(self.heartbeat,
                                                  self.heartbeat))
        self.connect()

    def connect(self):
        self.logger.debug('Connecting.')
        # based on the documentation at:
        # https://github.com/jasonrbriggs/stomp.py/wiki/Simple-Example
        self._conn.start()
        self._conn.connect(wait=True)
        self.logger.debug('Connected.')

    def shutdown(self):
        if self._conn:
            self._conn.disconnect()

    def process(self):
        event = self.receive_message()

        body = self.export_event(event)

        self._conn.send(body=body,
                        destination=self.exchange)
        self.acknowledge_message()


BOT = StompOutputBot
