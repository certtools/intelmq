# -*- coding: utf-8 -*-
"""
TODO: IPv6 See https://abusix.com/contactdb.html
"""
from __future__ import unicode_literals
import re

import dns.resolver
import intelmq.lib.harmonization as harmonization

QUERY_TEMPLATE = "%s.%s.%s.%s.abuse-contacts.abusix.org"
REGEX = r"[^@]+@[^@]+\.[^@]+"


class Abusix():

    @staticmethod
    def query(ip):

        if harmonization.IPAddress.version(ip) == 6:
            return None

        octets = ip.split('.')
        if len(octets) != 4:
            return None

        query = QUERY_TEMPLATE % (octets[3], octets[2], octets[1], octets[0])

        try:
            response = dns.resolver.query(query, 'TXT')
            if len(response) >= 1 and re.match(REGEX, str(response[0])):
                return str(response[0]).replace("\"", "")
            else:
                return None
        except:
            return None
