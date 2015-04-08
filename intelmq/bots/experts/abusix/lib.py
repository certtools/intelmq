import re
import dns.resolver 

class Abusix():

    @staticmethod
    def query(ip):

        ipbytes = ip.split('.')
        if len(ipbytes) != 4:
	    return None
	
	query = ipbytes[3] + '.' + ipbytes[2] + '.' + ipbytes[1] + '.' + ipbytes[0] + '.abuse-contacts.abusix.org'

        try:
            response = dns.resolver.query(query, 'TXT')
            if len(response) >= 1 and re.match(r"[^@]+@[^@]+\.[^@]+", str(response[0])):
                return str(response[0]).replace("\"", "")              
            else:
                return None
        except:
            return None
