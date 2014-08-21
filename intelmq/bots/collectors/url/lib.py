import re
import ssl
import socket
import shutil
import httplib
import urllib2
import StringIO
from urlparse import urlparse
from intelmq.lib.utils import decode

def fetch_url(url, timeout=60.0, chunk_size=16384):
    req = urllib2.urlopen(url, timeout = timeout)
    iostring = StringIO.StringIO()
    shutil.copyfileobj(req, iostring, chunk_size)
    value = iostring.getvalue()
    iostring.close()
    return decode(value, force=True)


def fetch_url_ssl(url, timeout=60.0, chunk_size=16384, key_file, cert_file, ca_file):
    
    url_parsed = urlparse(url)
    regex = '([^:]+)(:([0-9]+))?'

    host_port = re.search(regex, url_parsed.netloc)
    host = host_port.group(1)
    port = host_port.group(3)
    if not port:
        port = 443

    connection = HTTPSClientAuthConnection(host, port, key_file=key_file, cert_file=cert_file, ca_file=ca_file, timeout=60.0)
    connection.request('GET', url_parsed.path)   

    iostring = StringIO.StringIO()
    shutil.copyfileobj(connection.getresponse(), iostring, chunk_size)
    data = iostring.getvalue()

    iostring.close()
    connection.close()

    return data



class HTTPSClientAuthConnection(httplib.HTTPSConnection):

    def __init__(self, host, port, key_file, cert_file, ca_file, timeout=None):
        httplib.HTTPSConnection.__init__(self, host, key_file=key_file, cert_file=cert_file)
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_file = ca_file
        self.timeout = timeout
        self.cert_reqs = ssl.CERT_REQUIRED

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)

        if not self.ca_file:
            self.cert_reqs=ssl.CERT_NONE

        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ca_certs=self.ca_file, cert_reqs=self.cert_reqs)
