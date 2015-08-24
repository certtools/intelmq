import re

import dns.resolver

QUERY_TEMPLATE = "%s.%s.%s.%s.abuse-contacts.abusix.org"
REGEX = r"[^@]+@[^@]+\.[^@]+"


class Abusix():

    @staticmethod
    def query(ip):

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
