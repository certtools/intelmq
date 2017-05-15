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
http_proxy, https_proxy: string
strip_lines: boolean
http_timeout_sec: tuple of two floats or float
"""

import requests

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import decode


class HTTPStreamCollectorBot(CollectorBot):

    sighup_delay = False

    def init(self):
        if getattr(self.parameters, 'url', False) and \
           not getattr(self.parameters, 'http_url', False):
            self.logger.warning("Parameter 'url' is deprecated, use 'http_url' instead.")
            self.parameters.http_url = self.parameters.url
        self.set_request_parameters()

    def process(self):
        self.logger.info("Connecting to stream at %r.", self.parameters.http_url)

        try:
            req = requests.get(url=self.parameters.http_url, auth=self.auth,
                               proxies=self.proxy, headers=self.http_header,
                               verify=self.http_verify_cert,
                               cert=self.ssl_client_cert, stream=True,
                               timeout=self.http_timeout_sec)
        except requests.exceptions.ConnectionError:
            self.logger.exception('Connection Failed.')
        else:
            if req.status_code // 100 != 2:
                raise ValueError('HTTP response status code was {}.'
                                 ''.format(req.status_code))

            for line in req.iter_lines():
                if self.parameters.strip_lines:
                    line = line.strip()

                if not line:
                    # filter out keep-alive new lines and empty lines
                    continue

                report = self.new_report()
                report.add("raw", decode(line))
                report.add("feed.url", self.parameters.http_url)
                self.send_message(report)
            self.logger.info('Stream stopped.')


BOT = HTTPStreamCollectorBot
