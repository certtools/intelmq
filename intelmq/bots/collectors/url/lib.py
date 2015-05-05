import re
import ssl
import socket
import shutil
import http.client
import urllib.request, urllib.error, urllib.parse
import io
from urllib.parse import urlparse
from intelmq.lib.utils import decode

def fetch_url(url, timeout=60.0, chunk_size=16384, http_proxy = None, https_proxy = None):
    
    if http_proxy and https_proxy:
        proxy = urllib.request.ProxyHandler({'http': http_proxy, 'https': https_proxy })
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)

    req = urllib.request.urlopen(url, timeout = timeout)
    iostring = io.BytesIO()
    shutil.copyfileobj(req, iostring, chunk_size)
    value = iostring.getvalue()
    iostring.close()
    return decode(value)
