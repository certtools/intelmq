import dns
import socket
import urlparse

def is_ip(ip):
    if is_ipv4(ip):
        return True
    if is_ipv6(ip):
        return True
    return False


def is_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False

def is_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False

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

def reverse_ip(ip):
    import dns.reversename
    result = str(dns.reversename.from_address(ip))
    reverse = result.split('.in-addr.arpa.')
    if not reverse:
        reverse = result.split('.ip6.arpa.')
    return reverse[0]

def is_url(url, force_http = False):
    from urlparse import urlparse  

    res = urlparse(url)
    if not res.netloc == "":
        return True

    if force_http:
        res = urlparse("http://" + url)
        if not res.netloc == "":
            return True
    
    return False

# FIXME: is not correct.
def is_domain_name(domain_name):
    return not is_url(domain_name)