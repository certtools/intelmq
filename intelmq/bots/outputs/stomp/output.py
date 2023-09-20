# SPDX-FileCopyrightText: 2016 Mauro Silva
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

from intelmq.lib.bot import OutputBot
from intelmq.lib.mixins import StompMixin

try:
    import stomp
except ImportError:
    stomp = None


class StompOutputBot(OutputBot, StompMixin):
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
    auth_by_ssl_client_certificate: bool = True
    username: str = 'guest'  # ignored if `auth_by_ssl_client_certificate` is true
    password: str = 'guest'  # ignored if `auth_by_ssl_client_certificate` is true
    ssl_ca_certificate: str = 'ca.pem'  # TODO: could be pathlib.Path
    ssl_client_certificate: str = 'client.pem'  # TODO: pathlib.Path
    ssl_client_certificate_key: str = 'client.key'  # TODO: patlib.Path

    _conn = None

    def init(self):
        self.stomp_bot_runtime_initial_check()
        (self._conn,
         self._connect_kwargs) = self.prepare_stomp_connection()
        self.connect()

    def connect(self):
        self.logger.debug('Connecting.')
        # based on the documentation at:
        # https://github.com/jasonrbriggs/stomp.py/wiki/Simple-Example
        if stomp.__version__ < (4, 1, 20):
            self._conn.start()
        self._conn.connect(**self._connect_kwargs)
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

    @classmethod
    def check(cls, parameters):
        return cls.stomp_bot_parameters_check(parameters) or None


BOT = StompOutputBot
