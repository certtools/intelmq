# -*- coding: utf-8 -*-
"""
HTTP collector bot

Parameters:
http_url: string
http_header: dictionary
    default: {}
http_verify_cert: boolean
    default: True
http_username, http_password: string
http_proxy, http_ssl_proxy: string

"""
from __future__ import unicode_literals
import requests
import sys
import io
import zipfile

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report

# SNI Workaround for Python 2:
# https://github.com/kennethreitz/requests/blob/master/requests/packages/urllib3/contrib/pyopenssl.py#L16
try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass


class HTTPCollectorBot(Bot):

    def init(self):
        self.http_header = getattr(self.parameters, 'http_header', {})
        self.http_verify_cert = getattr(self.parameters, 'http_verify_cert',
                                        True)

        if hasattr(self.parameters, 'http_username') and hasattr(
                self.parameters, 'http_password'):
            self.auth = (self.parameters.http_username,
                         self.parameters.http_password)
        else:
            self.auth = None

        http_proxy = getattr(self.parameters, 'http_proxy', None)
        https_proxy = getattr(self.parameters, 'http_ssl_proxy', None)
        if http_proxy and https_proxy:
            self.proxy = {'http': http_proxy, 'https': https_proxy}
        else:
            self.proxy = None

        self.http_header['User-agent'] = self.parameters.http_user_agent

    def process(self):
        self.logger.info("Downloading report from %s" %
                         self.parameters.http_url)

        resp = requests.get(url=self.parameters.http_url, auth=self.auth,
                            proxies=self.proxy, headers=self.http_header,
                            verify=self.http_verify_cert)

        if resp.status_code // 100 != 2:
            raise ValueError('HTTP response status code was {}.'
                             ''.format(resp.status_code))

        self.logger.info("Report downloaded.")

        raw_reports = []
        try:
            zfp = zipfile.ZipFile(io.BytesIO(resp.content), "r")
        except zipfile.BadZipfile:
            raw_reports.append(resp.text)
        else:
            self.logger.info('Downloaded zip file, extracting following files:'
                             ' ' + ', '.join(zfp.namelist()))
            for filename in zfp.namelist():
                raw_reports.append(zfp.read(filename))

        for raw_report in raw_reports:
            report = Report()
            report.add("raw", raw_report)
            report.add("feed.name", self.parameters.feed)
            report.add("feed.url", self.parameters.http_url)
            report.add("feed.accuracy", self.parameters.accuracy)
            self.send_message(report)


if __name__ == "__main__":
    bot = HTTPCollectorBot(sys.argv[1])
    bot.start()
