# -*- coding: utf-8 -*-
"""
N6 STOMP collector bot

Parameters:
host:                          string
port:                          number
ssl_ca_certificate:            string (path)
ssl_client_certificate:        string (path)
ssl_client_certificate_key:    string (path)
heartbeats:                    number (default 60000)
"""
from __future__ import unicode_literals
import sys
import stomp

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report






class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        try:
            print message
        except:
            pass






class N6STOMPCollectorBot(Bot):

    def init(self):
        self.host = getattr(self.parameters, 'host', 'n6stream.cert.pl')
        self.port = getattr(self.parameters, 'port', 61614)
        self.heartbeat = getattr(self.parameters, 'heartbeat', 60000)
        self.ssl_ca_certificate = getattr(self.parameters, 'ssl_ca_certificate')
        self.ssl_client_certificate = getattr(self.parameters, 'ssl_client_certificate')
        self.ssl_client_certificate_key = getattr(self.parameters, 'ssl_client_certificate_key')
        self.http_verify_cert = getattr(self.parameters, 'http_verify_cert', True)

        _host = [(self.host, self.port)]
        self.conn = stomp.Connection(host_and_ports=_host, 
            use_ssl=True, ssl_key_file=self.ssl_client_certificate_key,
            ssl_cert_file=self.ssl_client_certificate,
            ssl_ca_certs=self.ssl_ca_certificate, heartbeats=(self.heartbeat, self.heartbeat))

        self.conn.set_listener('', MyListener())
        self.conn.set_listener('', PrintingListener())
        self.conn.start()
        self.conn.connect(wait=False)
        self.conn.subscribe(destination='/destination:/exchange/cert.at', id=1, ack='auto')


        http_proxy = getattr(self.parameters, 'http_proxy', None)
        https_proxy = getattr(self.parameters, 'http_ssl_proxy', None)
        if http_proxy and https_proxy:
            self.proxy = {'http': http_proxy, 'https': https_proxy}
        else:
            self.proxy = None

        self.http_header['User-agent'] = self.parameters.http_user_agent

    def disconnect():
        self.conn.disconnect()


    def process(self):
        pass

if __name__ == "__main__":
    bot = N6STOMPCollectorBot(sys.argv[1])
    bot.start()
