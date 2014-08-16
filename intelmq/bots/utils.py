import re
import dns
import socket
import binascii
from urlparse import urlparse


def get_domain_from_url():
    '''TBD'''


def get_ip_from_domain_name():
    '''TBD'''


def is_url(url):
   
    if not "/" in url:
        return None
    
    res = urlparse(url)
    if res.netloc != "":
        return url

    res = urlparse("http://" + url)
    if res.netloc != "":
        return "http://" + url
        
    return None


def is_domain_name(domain_name):
    
    if "/" in domain_name or not re.search('[a-zA-Z]', domain_name):
        return None

    res = urlparse(domain_name)
    if res.netloc != "":
        return domain_name

    res = urlparse("http://" + domain_name)
    if res.netloc != "":
        return domain_name

    return None


def is_ip(ip):
    if is_ipv4(ip):
        return ip
    if is_ipv6(ip):
        return ip
    return None


def is_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return ip
    except socket.error:
        return None


def is_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return ip
    except socket.error:
        return None


def ip_to_int(ip):
    try:
        ip_integer = socket.inet_pton(socket.AF_INET, ip)
    except socket.error:
        try:
            ip_integer = socket.inet_pton(socket.AF_INET6, ip)
        except socket.error:
            return None
        
    ip_integer = int(binascii.hexlify(ip_integer), 16)
    return ip_integer    


def get_reverse_ip(ip):
    result = str(dns.reversename.from_address(ip))
    reverse = result.split('.in-addr.arpa.')
    if not reverse:
        reverse = result.split('.ip6.arpa.')
    return reverse[0]



# [FIXME - Review]
def source_time(event, key):
    value = event.value(key)
    new_value = dateparser.parse(value).isoformat()
    event.discard(key, value)
    event.add(key, new_value)
    return event

# [FIXME - Review]
def generate_source_time(event, key):        
    value = datetime.datetime.utcnow()
    value = value.replace(hour=0,minute=0,second=0,microsecond=0)
    value = value.isoformat()
    event.add(key, value)
    return event

# [FIXME - Review]
def generate_observation_time(event, key):        
    value = datetime.datetime.utcnow()
    value = value.replace(microsecond=0)
    value = value.isoformat()
    event.add(key, value)
    return event