import binascii
import StringIO
import dns.resolver
from intelmq.lib.utils import decode
from intelmq.bots import utils

'''
Reference: http://www.team-cymru.org/Services/ip-to-asn.html#dns
'''

IP_QUERY  = "%s.origin%s.asn.cymru.com"
ASN_QUERY = "AS%s.asn.cymru.com"

class Cymru():

   
    @staticmethod
    def query(ip, ip_version):
        raw_result = Cymru.__ip_query(ip, ip_version)
        result     = Cymru.__ip_query_parse(raw_result)
        if "asn" in result:
            raw_result  = Cymru.__asn_query(result['asn'])
            extra_info  = Cymru.__asn_query_parse(raw_result)
            result.update(extra_info)

        return result


    @staticmethod
    def __query(query):    
        try:
            for query_result in dns.resolver.query(query, rdtype='TXT'):    
                fp = StringIO.StringIO()
                query_result.to_wire(fp)
                value = fp.getvalue()[1:] # ignore first character
                fp.close()
                return decode(value, force=True)
            
        except dns.exception.DNSException:
            return None


    @staticmethod
    def __ip_query(ip, ip_version):      
        reversed_ip = utils.get_reverse_ip(ip)
        version = ""
        if ip_version == 6:
            version = "6"
            
        query = IP_QUERY % (reversed_ip, version)
        return Cymru.__query(query)

        
    @staticmethod
    def __asn_query(asn):
        query = ASN_QUERY % (asn)
        return Cymru.__query(query)
    
    
    @staticmethod
    def __query_parse(text):
        items = list()
        for item in text.split('|'):
            item = item.replace('"','')
            item = item.strip()
            if item == "NA" or item == "":
                item = None
            items.append(item)
        return items
    

    @staticmethod    
    def __ip_query_parse(text):
        
        # Example:   "1930       | 193.136.0.0/15  | PT | ripencc |"
        # Exception: "9395 17431 | 219.234.80.0/20 | CN | apnic   | 2002-04-17"

        result = dict()

        if not text:
            return result
        
        items = Cymru.__query_parse(text)

        if items[0]:
            asn = items[0].split(' ')[0]  # In case of multiple ASNs received, get the first one.
            try:
                int(asn)
                result['asn'] = asn
            except:
                pass
            
        if items[1]:    
            result['bgp_prefix'] = items[1]
        
        if items[2]:    
            result['cc'] = items[2]

        if items[3]:    
            result['registry'] = items[3]

        if items[4]:    
            result['allocated'] = items[4]

        return result


    @staticmethod    
    def __asn_query_parse(text):
        
        # Example:   "23028 | US | arin    | 2002-01-04 | TEAM-CYMRU - Team Cymru Inc.,US"
        # Exception: "1930  | EU | ripencc |            | RCCN Rede Ciencia Tecnologia e Sociedade (RCTS),PT"

        result = dict()

        if not text:
            return result
        
        items = Cymru.__query_parse(text)
        
        if items[4]:    
            result['as_name'] = items[4]

        return result    

