import re
import dns
import pytz
import socket
import binascii
import datetime
import dateutil.parser
import dateutil.tz
from urlparse import urlparse


def get_domain_name_from_url(url):
    res = urlparse(url)
    if res.netloc != "" and not is_ip(res.netloc):
        return res.netloc
    return None


def get_ip_from_url(url):
    res = urlparse(url)
    if res.netloc != "":
        return get_ip_from_domain_name(res.netloc)
    return None


def get_ip_from_domain_name(domain_name):
    try:
        socket.setdefaulttimeout(0.5)
        return socket.gethostbyname(domain_name)
    except:
        return None


def get_reverse_ip(ip):
    result = str(dns.reversename.from_address(ip))
    reverse = result.split('.in-addr.arpa.')
    if not reverse:
        reverse = result.split('.ip6.arpa.')
    return reverse[0]


def is_url(url):
   
    if not "/" in url:
        return None
    
    if "hxxp://" in url:
        url = url.replace('hxxp://','http://')
    
    if "hxxps://" in url:
        url = url.replace('hxxps://','https://')
    
    res = urlparse(url)
    if res.netloc != "":
        return url

    res = urlparse("http://" + url)
    if res.netloc != "":
        return "http://" + url
        
    return None


def is_domain_name(domain_name):
    
    if "/" in domain_name or is_ip(domain_name):
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


def parse_source_time(event, key):
    if not event.contains(key):
        return generate_source_time(event, key)
    
    value = event.value(key)
    event.discard(key, value)
    
    new_value = dateutil.parser.parse(value)
    new_value = new_value.astimezone(pytz.utc)
    new_value = new_value.isoformat()
    event.add(key, new_value)
    return event


def generate_source_time(event, key):        
    value = datetime.datetime.utcnow()
    tz = pytz.timezone('UTC')
    value = value.replace(hour=0,minute=0,second=0,microsecond=0, tzinfo=tz)
    value = value.isoformat()
    event.add(key, value)
    return event


def generate_observation_time(event, key):        
    value = datetime.datetime.utcnow()
    value = value.replace(microsecond=0)
    value = value.isoformat()
    event.add(key, value)
    return event


def generate_reported_fields(event):
    
    keys_pairs = [
                    (
                        "source_ip",
                        "source_domain_name",
                        "source_url",
                        "source_email_address",
                        "source_asn",
                        "source_cc"
                    ),
                    (
                        "destination_ip",
                        "destination_domain_name",
                        "destination_url",
                        "destination_email_address",
                        "destination_asn",
                        "destination_cc"
                    )
                 ]

    for keys in keys_pairs:
        for key in keys:
            if event.contains(key):
                value = event.value(key)
                reported_key = "reported_%s" % key
                event.add(reported_key, value)
                
    return event
