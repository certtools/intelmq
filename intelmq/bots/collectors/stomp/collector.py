# -*- coding: utf-8 -*-
import os.path

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import stomp
except ImportError:
    stomp = None
else:
    class StompListener(stomp.PrintingListener):
        """
        the stomp listener gets called asynchronously for
        every STOMP message
        """
        def __init__(self, n6stompcollector, conn, destination):
            self.stompbot = n6stompcollector
            self.conn = conn
            self.destination = destination
            super().__init__()
            if stomp.__version__ >= (5, 0, 0):
                # set the function directly, as the argument print_to_log logs to the generic logger
                self._PrintingListener__print = n6stompcollector.logger.debug

        def on_heartbeat_timeout(self):
            self.stompbot.logger.info("Heartbeat timeout. Attempting to re-connect.")
            connect_and_subscribe(self.conn, self.stompbot.logger, self.destination)

        def on_error(self, headers, message):
            self.stompbot.logger.error('Received an error: %r.', message)

        def on_message(self, headers, message):
            self.stompbot.logger.debug('Receive message %r...', message[:500])
            report = self.stompbot.new_report()
            report.add("raw", message.rstrip())
            report.add("feed.url", "stomp://" +
                       self.stompbot.parameters.server +
                       ":" + str(self.stompbot.parameters.port) +
                       "/" + self.stompbot.parameters.exchange)
            self.stompbot.send_message(report)

        def on_disconnected(self):
            self.stompbot.logger.debug('Detected disconnect')
            connect_and_subscribe(self.conn, self.stompbot.logger, self.destination)


def connect_and_subscribe(conn, logger, destination, start=False):
    if start:
        conn.start()
    conn.connect(wait=True)
    conn.subscribe(destination=destination,
                   id=1, ack='auto')
    logger.info('Successfully connected and subscribed.')


class StompCollectorBot(CollectorBot):
    """ main class for the STOMP protocol collector """

    collector_empty_process = True
    conn = False  # define here so shutdown method can check for it

    def init(self):
        if stomp is None:
            raise MissingDependencyError("stomp")
        elif stomp.__version__ < (4, 1, 8):
            raise MissingDependencyError("stomp", version="4.1.8",
                                         installed=stomp.__version__)

        self.server = getattr(self.parameters, 'server', 'n6stream.cert.pl')
        self.port = getattr(self.parameters, 'port', 61614)
        self.exchange = getattr(self.parameters, 'exchange', '')
        self.heartbeat = getattr(self.parameters, 'heartbeat', 60000)
        self.ssl_ca_cert = getattr(self.parameters, 'ssl_ca_certificate',
                                   'ca.pem')
        self.ssl_cl_cert = getattr(self.parameters, 'ssl_client_certificate',
                                   'client.pem')
        self.ssl_cl_cert_key = getattr(self.parameters,
                                       'ssl_client_certificate_key',
                                       'client.key')
        self.http_verify_cert = getattr(self.parameters,
                                        'http_verify_cert', True)

        # check if certificates exist
        for f in [self.ssl_ca_cert, self.ssl_cl_cert, self.ssl_cl_cert_key]:
            if not os.path.isfile(f):
                raise ValueError("Could not open file %r." % f)

        _host = [(self.server, self.port)]
        self.conn = stomp.Connection(host_and_ports=_host, use_ssl=True,
                                     ssl_key_file=self.ssl_cl_cert_key,
                                     ssl_cert_file=self.ssl_cl_cert,
                                     ssl_ca_certs=self.ssl_ca_cert,
                                     heartbeats=(self.heartbeat,
                                                 self.heartbeat))

        self.conn.set_listener('', StompListener(self, self.conn, self.exchange))
        connect_and_subscribe(self.conn, self.logger, self.exchange,
                              start=stomp.__version__ < (4, 1, 20))

    def shutdown(self):
        if not stomp or not self.conn:
            return
        try:
            self.conn.disconnect()
        except stomp.exception.NotConnectedException:
            pass

    def process(self):
        pass


BOT = StompCollectorBot
