# -*- coding: utf-8 -*-
"""
TODO: Test this with a real stomp server
"""
import os.path

from intelmq.lib.bot import Bot
from intelmq.lib.message import MessageFactory

try:
    import stomp
except ImportError:
    stomp = None


class StompOutputBot(Bot):
    """ main class for the STOMP protocol output bot """

    def init(self):
        if stomp is None:
            raise ValueError('Could not import stomp. Please install it.')

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
                                     wait_on_receipt=True,
                                     heartbeats=(self.heartbeat,
                                                 self.heartbeat))

        # based on the documentation at:
        # https://github.com/jasonrbriggs/stomp.py/wiki/Simple-Example
        self.conn.start()
        self.conn.connect(wait=False)

    def shutdown(self):
        self.conn.disconnect()

    def process(self):
        message = self.receive_message()
        message = MessageFactory.serialize(message)
        self.conn.send(body=message, destination=self.exchange)
        self.acknowledge_message()


BOT = StompOutputBot
