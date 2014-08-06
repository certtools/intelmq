import urllib2
import urllib
import shutil
import logging
import hashlib
import socket
import binascii
import StringIO

def decode(text, encodings=["utf-8", "ascii"], force=False):
    for encoding in encodings:
        try:
            return text.decode(encoding)
        except ValueError as e:
            pass
        
    if force:
        for encoding in encodings:
            try:
                return text.decode(encoding, 'ignore')
            except ValueError as e:
                pass

    raise Exception("Found a problem when decoding.")


def encode(text, encodings=["utf-8", "ascii"], force=False):
    for encoding in encodings:
        try:
            return text.encode(encoding)
        except ValueError as e:
            pass
        
    if force:
        for encoding in encodings:
            try:
                return text.decode(encoding, 'ignore')
            except ValueError as e:
                pass

    raise Exception("Found a problem when encoding.")


def fetch_url(url, timeout=60.0, chunk_size=16384):
    req = urllib2.urlopen(url, timeout = timeout)
    strio = StringIO.StringIO()
    shutil.copyfileobj(req, strio, chunk_size)
    value = strio.getvalue()
    strio.close()
    return decode(value, force=True)


def fetch_imap(server, username, password, ssl, folder, unread, sent_from, sent_to, subject, max_emails):
    '''
        Additional information: https://github.com/martinrusev/imbox
    '''

    emails = list()
    
    if not max_emails:
        max_emails = 1

    mailbox = Imbox(server, username, password, ssl)
    messages_folder = mailbox.messages(folder=folder, unread=unread, sent_from=sent_from, sent_to=sent_to)

    counter = 0
    for uid, message in messages_folder:

        if max_emails <= counter:
            return emails

        email = dict()
    
        if subject and not subject in message.subject:
            continue
        
        emails.append(message)
        counter += 1
        
    return emails


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



