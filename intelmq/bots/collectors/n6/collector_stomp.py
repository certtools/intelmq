# -*- coding: utf-8 -*-
import os.path

from intelmq.lib.bot import CollectorBot

try:
    import stomp

    class StompListener(stomp.listener.PrintingListener):
        """ the stomp listener gets called asynchronously for
            every STOMP message
        """
        def __init__(self, n6stompcollector):
            self.n6stomper = n6stompcollector

        def on_heartbeat_timeout(self):
            self.n6stomper.logger.warn("Heartbeat timeout. Attempting to re-connect.")
            self.n6stomper.conn.disconnect()
            status = self.n6stomper.conn.connect(wait=False)
            self.n6stomper.logger.info("Re-connected: %s.", status)

        def on_error(self, headers, message):
            self.n6stomper.logger.error('Received an error: %r.', message)

        def on_message(self, headers, message):
            self.n6stomper.logger.debug('Receive message %r...', message[:500])
            report = self.n6stomper.new_report()
            report.add("raw", message.rstrip())
            report.add("feed.url", "stomp://" +
                       self.n6stomper.parameters.server +
                       ":" + str(self.n6stomper.parameters.port) +
                       "/" + self.n6stomper.parameters.exchange)
            self.n6stomper.send_message(report)
except ImportError:
    stomp = None


class n6stompCollectorBot(CollectorBot):
    """ main class for the n6 STOMP protocol collector """

    def init(self):
        if stomp is None:
            self.logger.error('Could not import stomp. Please install it.')
            self.stop()

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
                                     wait_on_receipt=True,
                                     heartbeats=(self.heartbeat,
                                                 self.heartbeat))

        self.conn.set_listener('', StompListener(self))
        self.conn.start()
        self.conn.connect(wait=False)
        self.conn.subscribe(destination=self.exchange, id=1, ack='auto')
        self.logger.info('Successfully connected and subscribed to %s:%s.',
                         self.server, self.port)

    def disconnect(self):
        self.conn.disconnect()

    def process(self):
        pass


BOT = n6stompCollectorBot
