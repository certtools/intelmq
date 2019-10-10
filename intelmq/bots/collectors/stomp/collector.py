# -*- coding: utf-8 -*-
import os.path

from intelmq.lib.bot import CollectorBot

try:
    import stomp
except ImportError:
    stomp = None
else:
    class StompListener(stomp.listener.PrintingListener):
        """
        the stomp listener gets called asynchronously for
        every STOMP message
        """
        def __init__(self, n6stompcollector):
            self.stompbot = n6stompcollector

        def on_heartbeat_timeout(self):
            self.stompbot.logger.info("Heartbeat timeout. Attempting to re-connect.")
            self.connect_and_subscribe()

        def connect_and_subscribe(self):
            self.conn.start()
            connect_status = self.conn.connect(wait=True)
            subscribe_status = self.conn.subscribe(destination=self.destination,
                                                   id=1, ack='auto')
            self.stompbot.logger.info('Successfully connected and subscribed. '
                                      'Connect status: %r, subscribe status: %r.',
                                      connect_status, subscribe_status)

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
            self.connect_and_subscribe()



class StompCollectorBot(CollectorBot):
    """ main class for the STOMP protocol collector """

    collector_empty_process = True

    def init(self):
        if stomp is None:
            raise ValueError('Could not import stomp. Please install it.')

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
        self.conn.destination = self.exchange
        self.conn.connect_and_subscribe()

    def shutdown(self):
        try:
            self.conn.disconnect()
        except stomp.exception.NotConnectedException:
            pass

    def process(self):
        pass


BOT = StompCollectorBot
