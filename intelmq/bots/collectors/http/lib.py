# -*- coding: utf-8 -*-
import shutil
import StringIO
import urllib2


def fetch_url(url, timeout=60.0, chunk_size=16384, http_proxy=None,
              https_proxy=None, user_agent=None):

    if http_proxy and https_proxy:
        proxy = urllib2.ProxyHandler(
            {'http': http_proxy, 'https': https_proxy})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    req = urllib2.Request(url)

    if not user_agent:
        user_agent = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

    req.add_header('User-agent', user_agent)
    resp = urllib2.urlopen(req, timeout=timeout)

    iostring = StringIO.StringIO()
    shutil.copyfileobj(resp, iostring, chunk_size)
    value = iostring.getvalue()
    iostring.close()

    return value
