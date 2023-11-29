# SPDX-FileCopyrightText: 2016 Mauro Silva
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

try:
    import stomp
except ImportError:
    stomp = None

from intelmq.lib.bot import OutputBot
from intelmq.lib.mixins import StompMixin


class StompOutputBot(OutputBot, StompMixin):
    """Send events to a STMOP server"""
    """ main class for the STOMP protocol output bot """

    http_verify_cert = True
    keep_raw_field: bool = False
    message_hierarchical_output: bool = False
    message_jsondict_as_string: bool = False
    message_with_type: bool = False
    single_key: bool = False

    server: str = '127.0.0.1'  # <- TODO: change to 'n6stream.cert.pl' (==StompCollectorBot.server)
    port: int = 61614
    exchange: str = '/exchange/_push'
    heartbeat: int = 60000

    # Note: the `ssl_ca_certificate` configuration parameter must be set:
    # * *either* to the server's CA certificate(s) file path,
    # * *or* to an empty string -- dictating that the SSL tools employed
    #   by the `stomp.py`'s machinery will attempt to load the system’s
    #   default CA certificates.
    # The latter, if applicable, is more convenient -- by avoiding the
    # need to manually update the CA certificate(s) file.
    ssl_ca_certificate: str = 'ca.pem'  # <- TODO: change to ''
    # (^ TODO: could also be pathlib.Path)

    auth_by_ssl_client_certificate: bool = True

    # Used if `auth_by_ssl_client_certificate` is true (otherwise ignored):
    ssl_client_certificate: str = 'client.pem'       # (cert file path)
    ssl_client_certificate_key: str = 'client.key'   # (cert's key file path)
    # (^ TODO: could also be pathlib.Path)

    # Used if `auth_by_ssl_client_certificate` is false (otherwise ignored):
    username: str = 'guest'   # (STOMP auth *login*)
    password: str = 'guest'   # (STOMP auth *passcode*)

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

        try:
            self._conn.send(body=body, destination=self.exchange)
        except stomp.exception.NotConnectedException:
            self.logger.warning("Detected connection error, trying to reestablish it.")
            self.connect()
            raise  # Fallback to default retry
        self.acknowledge_message()

    @classmethod
    def check(cls, parameters):
        return cls.stomp_bot_parameters_check(parameters) or None


BOT = StompOutputBot
