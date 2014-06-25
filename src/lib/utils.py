import urllib2
import urllib
import shutil
import logging
import hashlib
import socket
import binascii

def fetch_url(url, timeout=60.0, chunk_size=16384):
    # FIXME: change this code
    req = urllib2.urlopen(url, timeout = timeout)
    filename = "/tmp/temp.txt"
    with open(filename, 'wb') as fpw:
        shutil.copyfileobj(req, fpw, chunk_size)
    fpw.close()
    fpr = open(filename, 'r')
    return fpr.read()


def fetch_imap():
    '''__placeholder'''


def fetch_pgp():
    '''__placeholder'''


def hashgen(data, func=hashlib.sha1):
    result = func()
    result.update(data)
    return result.hexdigest()


def force_decode(string, encodings=["ascii", "utf-8"]):
    if isinstance(string, unicode):
        return string

    for encoding in encodings:
        try:
            return string.decode(encoding)
        except ValueError:
            pass
    return string.decode("latin-1", "replace")


def log(name, loglevel="DEBUG"):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    
    handler = logging.FileHandler("log/%s.log" % name)
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
