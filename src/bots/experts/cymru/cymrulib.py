import dns.resolver
import binascii
from lib.utils import *

# Reference: http://www.team-cymru.org/Services/ip-to-asn.html#dns

class Cymru():

    @staticmethod
    def query(ip, ip_version):
        asn = bgp = cc = registry = allocated = as_name = ""
        
        ip_query_result = Cymru.ip_query(ip, ip_version)
        asn, bgp, cc, registry, allocated = Cymru.parse(ip_query_result, "ip")
        
        if asn:
            asn_query_result = Cymru.asn_query(asn)
            as_name = Cymru.parse(asn_query_result, "asn")            
        
        return " | ".join([ asn, bgp, cc, registry, allocated, as_name ])

    @staticmethod
    def ip_query(ip, ip_version):
        reversed_ip = reverse_ip(ip)
        template_query = "%s.origin%s.asn.cymru.com"

        if ip_version == 4:
            query = template_query % (reversed_ip, "")
        else:
            query = template_query % (reversed_ip, str(ip_version))   

        try:
            for query_result in dns.resolver.query(query, rdtype='TXT'):
                return str(query_result)
        except dns.exception.DNSException:
            return " | | | | "
        
    @staticmethod    
    def asn_query(asn):
        template_query = "AS%s.asn.cymru.com"
        query = template_query % (asn)
        try:
            for query_result in dns.resolver.query(query, rdtype='TXT'):
                return str(query_result)
        except dns.exception.DNSException:
            return " | | | | "
        
    @staticmethod    
    def parse(text, type="all"):
        result = list()

        for item in text.split('|'):
            item = item.replace('"','')
            item = item.strip()
            
            if item == "-" or item == "":
                result.append(None)
            else:
                result.append(item)

        if type == "ip":
            return result    # [ asn, bgp, cc, registry, allocated ]
        elif type == "asn":
            return result[4] # [ as name ]
        else:
            return result    # [ asn, bgp, cc, registry, allocated, as name ]