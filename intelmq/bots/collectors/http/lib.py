# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests


def fetch_url(url, timeout=60.0, chunk_size=16384, http_proxy=None,
              https_proxy=None, user_agent=None, header={}, auth=None,
              verify_cert=True):

    if http_proxy and https_proxy:
        proxy = {'http': http_proxy, 'https': https_proxy}
    else:
        proxy = None

    if user_agent is not None:
        header['User-agent'] = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/"
                                "537.36 (KHTML, like Gecko) Chrome/41.0.2228.0"
                                " Safari/537.36")
    else:
        header['User-agent'] = user_agent

    resp = requests.get(url=url, auth=auth, timeout=timeout,
                        proxies=proxy, headers=header, verify=verify_cert)
    return resp.text
