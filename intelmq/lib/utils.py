import urllib2
import urllib
import shutil
import logging
import hashlib
import socket
import binascii
import StringIO

def fetch_url(url, timeout=60.0, chunk_size=16384):
    req = urllib2.urlopen(url, timeout = timeout)
    strio = StringIO.StringIO()
    shutil.copyfileobj(req, strio, chunk_size)
    value = strio.getvalue()
    strio.close()
    return value


def fetch_imap():
    '''__placeholder'''


def fetch_pgp():
    '''__placeholder'''


def hashgen(data, func=hashlib.sha1):
    result = func()
    result.update(data)
    return result.hexdigest()


def log(logs_path, name, loglevel="DEBUG"):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    
    handler = logging.FileHandler("%s/%s.log" % (logs_path, name))
    handler.setLevel(loglevel)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)    
    return logger  


def post_url(url, data, timeout=60.0, chunk_size=16384):
    encoded_data = urllib.urlencode(data)
    req = urllib2.urlopen(url, encoded_data, timeout)
    return req.read()

def is_ip(ip):
    try:
        ip_integer = socket.inet_pton(socket.AF_INET, ip)
        ip_version = 4
    except socket.error:
        try:
            ip_integer = socket.inet_pton(socket.AF_INET6, ip)
            ip_version = 6
        except socket.error:
            return None
        
    ip_integer = int(binascii.hexlify(ip_integer), 16)
    return [ ip , ip_version, ip_integer ]

def reverse_ip(ip):
    import dns.reversename
    result = str(dns.reversename.from_address(ip))
    reverse = result.split('.in-addr.arpa.')
    if not reverse:
        reverse = result.split('.ip6.arpa.')
    return reverse[0]


def decode(text, encodings=["ascii", "utf-8"]):
    if not isinstance(text, basestring):
        return None

    if isinstance(text, unicode):
        return text

    for encoding in encodings:
        try:
            return unicode(text, encoding)
        except ValueError as e:
            pass

    return None 