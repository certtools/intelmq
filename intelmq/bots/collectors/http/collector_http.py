# -*- coding: utf-8 -*-
"""
HTTP collector bot

Parameters:
url: string
http_header: dictionary
    default: {}
verify_cert: boolean
    default: True
username, password: string
http_proxy, https_proxy: string

"""
from __future__ import unicode_literals
import requests
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


class HTTPCollectorBot(Bot):

    def init(self):
        self.http_header = getattr(self.parameters, 'http_header', {})
        self.verify_cert = getattr(self.parameters, 'verify_cert', True)

        if hasattr(self.parameters, 'username') and hasattr(self.parameters,
                                                            'password'):
            self.auth = (self.parameters.username, self.parameters.password)
        else:
            self.auth = None

        http_proxy = getattr(self.parameters, 'http_proxy', None)
        https_proxy = getattr(self.parameters, 'https_proxy', None)
        if http_proxy and https_proxy:
            self.proxy = {'http': http_proxy, 'https': https_proxy}
        else:
            self.proxy = None

        self.http_header['User-agent'] = self.parameters.http_user_agent

    def process(self):
        self.logger.info("Downloading report from %s" % self.parameters.url)

        resp = requests.get(url=self.parameters.url, auth=self.auth,
                            proxies=self.proxy, headers=self.http_header,
                            verify=self.verify_cert)

        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", resp.text, sanitize=True)
        report.add("feed.name", self.parameters.feed, sanitize=True)
        report.add("feed.url", self.parameters.url, sanitize=True)
        time_observation = DateTime().generate_datetime_now()
        report.add('time.observation', time_observation, sanitize=True)
        self.send_message(report)


if __name__ == "__main__":
    bot = HTTPCollectorBot(sys.argv[1])
    bot.start()
