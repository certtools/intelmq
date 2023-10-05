# SPDX-FileCopyrightText: 2017 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

try:
    import stomp
except ImportError:
    stomp = None
else:
    import stomp.exception

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import StompMixin


if stomp is not None:

    class StompListener(stomp.PrintingListener):
        """
        the stomp listener gets called asynchronously for
        every STOMP message
        """
        def __init__(self, n6stompcollector, conn, destination, connect_kwargs=None):
            self.stompbot = n6stompcollector
            self.conn = conn
            self.connect_kwargs = connect_kwargs
            self.destination = destination
            super().__init__()
            if stomp.__version__ >= (5, 0, 0):
                # set the function directly, as the argument print_to_log logs to the generic logger
                self._PrintingListener__print = n6stompcollector.logger.debug

        def on_heartbeat_timeout(self):
            self.stompbot.logger.info("Heartbeat timeout. Attempting to re-connect.")
            if self.stompbot._auto_reconnect:
                connect_and_subscribe(self.conn, self.stompbot.logger, self.destination,
                                      connect_kwargs=self.connect_kwargs)

        def on_error(self, frame, body=None):
            if body is None:
                # `stomp.py >= 6.1.0`
                body = frame.body
            self.stompbot.logger.error('Received an error: %r.', body)

        def on_message(self, frame, body=None):
            if body is None:
                # `stomp.py >= 6.1.0`
                body = frame.body
            self.stompbot.logger.debug('Receive message %r...', body[:500])
            report = self.stompbot.new_report()
            report.add("raw", body.rstrip())
            report.add("feed.url", "stomp://" +
                       self.stompbot.server +
                       ":" + str(self.stompbot.port) +
                       "/" + self.stompbot.exchange)
            self.stompbot.send_message(report)

        def on_disconnected(self):
            self.stompbot.logger.debug('Detected disconnect')
            if self.stompbot._auto_reconnect:
                connect_and_subscribe(self.conn, self.stompbot.logger, self.destination,
                                      connect_kwargs=self.connect_kwargs)


def connect_and_subscribe(conn, logger, destination, start=False, connect_kwargs=None):
    if start:
        conn.start()
    if connect_kwargs is None:
        connect_kwargs = dict(wait=True)
    conn.connect(**connect_kwargs)
    conn.subscribe(destination=destination,
                   id=1, ack='auto')
    logger.info('Successfully connected and subscribed.')


class StompCollectorBot(CollectorBot, StompMixin):
    """Collect data from a STOMP Interface"""
    """ main class for the STOMP protocol collector """

    server: str = 'n6stream.cert.pl'
    port: int = 61614
    exchange: str = ''
    heartbeat: int = 6000

    # Note: the `ssl_ca_certificate` configuration parameter must be set:
    # * *either* to the server's CA certificate(s) file path,
    # * *or* to an empty string -- dictating that the SSL tools employed
    #   by the `stomp.py`'s machinery will attempt to load the system’s
    #   default CA certificates.
    # The latter, if applicable, is more convenient -- by avoiding the
    # need to manually update the CA certificate(s) file.
    ssl_ca_certificate: str = 'ca.pem'  # <- TODO: change to '' (+ remove "ca.pem*" legacy files)
    # (^ TODO: could also be pathlib.Path)

    auth_by_ssl_client_certificate: bool = True

    # Used if `auth_by_ssl_client_certificate` is true (otherwise ignored):
    ssl_client_certificate: str = 'client.pem'       # (cert file path)
    ssl_client_certificate_key: str = 'client.key'   # (cert's key file path)
    # (^ TODO: could also be pathlib.Path)

    # Used if `auth_by_ssl_client_certificate` is false (otherwise ignored):
    username: str = 'guest'   # (STOMP auth *login*)
    password: str = 'guest'   # (STOMP auth *passcode*)

    _collector_empty_process: bool = True
    __conn = False  # define here so shutdown method can check for it

    def init(self):
        self.stomp_bot_runtime_initial_check()

        # (note: older versions of `stomp.py` do not play well with reconnects)
        self._auto_reconnect = (stomp.__version__ >= (4, 1, 21))

        self.__conn, connect_kwargs = self.prepare_stomp_connection()
        self.__conn.set_listener('', StompListener(self, self.__conn, self.exchange,
                                                   connect_kwargs=connect_kwargs))
        connect_and_subscribe(self.__conn, self.logger, self.exchange,
                              start=stomp.__version__ < (4, 1, 20),
                              connect_kwargs=connect_kwargs)

    def shutdown(self):
        if not stomp or not self.__conn:
            return
        self._auto_reconnect = False
        try:
            self.__conn.disconnect()
        except stomp.exception.NotConnectedException:
            pass

    def process(self):
        pass

    @classmethod
    def check(cls, parameters):
        return cls.stomp_bot_parameters_check(parameters) or None


BOT = StompCollectorBot
