# -*- coding: utf-8 -*-
import os.path

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError


try:
    import stomp
except ImportError:
    stomp = None


class StompOutputBot(OutputBot):
    """ main class for the STOMP protocol output bot """

    conn = None

    def init(self):
        if stomp is None:
            raise MissingDependencyError("stomp")

        self.server = getattr(self.parameters, 'server', '127.0.0.1')
        self.port = getattr(self.parameters, 'port', 61614)
        self.exchange = getattr(self.parameters, 'exchange', '/exchange/_push')
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
                raise ValueError("Could not open SSL (certificate) file '%s'." % f)

        _host = [(self.server, self.port)]
        self.conn = stomp.Connection(host_and_ports=_host, use_ssl=True,
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
        self.conn.start()
        self.conn.connect(wait=True)
        self.logger.debug('Connected.')

    def shutdown(self):
        if self.conn:
            self.conn.disconnect()

    def process(self):
        event = self.receive_message()

        body = self.export_event(event)

        self.conn.send(body=body,
                       destination=self.exchange)
        self.acknowledge_message()


BOT = StompOutputBot
