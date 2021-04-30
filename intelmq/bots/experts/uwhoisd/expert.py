# -*- coding: utf-8 -*-

import socket
from urllib.parse import urlparse

from intelmq.lib.bot import Bot


class UniversalWhoisExpertBot(Bot):
    """ Universal Whois expert bot get the whois entry related an a domain,
    hostname, IP address, or ASN from a centralised uWhoisd instance """
    server: str = 'localhost'
    port: int = 4243

    def _whois(self, query: str) -> str:
        bytes_whois = b''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server, self.port))
            sock.sendall(f'{query}\n'.encode())
            while True:
                data = sock.recv(2048)
                if not data:
                    break
                bytes_whois += data
        to_return = bytes_whois.decode()
        return to_return

    def process(self):
        event = self.receive_message()
        if 'source.url' in event:
            parsed = urlparse(event.get('source.url'))
            query = parsed.hostname
        elif 'source.fqdn' in event:
            query = event.get('source.fqdn')
        elif 'source.ip' in event:
            query = event.get('source.ip')
        elif 'source.asn' in event:
            query = event.get('source.asn')
        else:
            query = None

        if query:
            whois_entry = self._whois(query)
            event.add('extra.whois', whois_entry)

        self.send_message(event)
        self.acknowledge_message()


BOT = UniversalWhoisExpertBot
