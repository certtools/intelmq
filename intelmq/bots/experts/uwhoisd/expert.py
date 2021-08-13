# SPDX-FileCopyrightText: 2021 Raphaël Vinot
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
        if 'source.url' in event or 'source.fqdn' in event:
            if 'source.fqdn' in event:
                query = event.get('source.fqdn')
            else:
                parsed = urlparse(event.get('source.url'))
                query = parsed.hostname
            whois_entry = self._whois(query)
            event.add('extra.whois.fqdn', whois_entry)
        if 'source.ip' in event:
            query = event.get('source.ip')
            whois_entry = self._whois(query)
            event.add('extra.whois.ip', whois_entry)
        if 'source.asn' in event:
            query = event.get('source.asn')
            whois_entry = self._whois(f'AS{query}')
            event.add('extra.whois.asn', whois_entry)

        self.send_message(event)
        self.acknowledge_message()


BOT = UniversalWhoisExpertBot
