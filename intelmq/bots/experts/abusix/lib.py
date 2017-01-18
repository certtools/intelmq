# -*- coding: utf-8 -*-
import ipaddress
import re

import dns.resolver

QUERY_HOST = ".abuse-contacts.abusix.org"
REGEX = r"[^@]+@[^@]+\.[^@]+"


class Abusix():

    @staticmethod
    def query(ip):

        if ipaddress.ip_address(ip).version == 6:
            addr = ipaddress.ip_address(ip).exploded
            rev = '.'.join(reversed(addr.replace(':', '')))
        else:
            rev = '.'.join(reversed(ip.split('.')))

        query = rev + QUERY_HOST

        try:
            response = dns.resolver.query(query, 'TXT')
            if len(response) >= 1 and re.match(REGEX, str(response[0])):
                return str(response[0]).replace("\"", "")
            else:
                return None
        except:
            return None
