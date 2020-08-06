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

try:
    import requests
except ImportError:
    requests = None

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import decode, create_request_session
from intelmq.lib.exceptions import MissingDependencyError


class HTTPStreamCollectorBot(CollectorBot):

    sighup_delay = False

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.set_request_parameters()
        self.session = create_request_session(self)

    def process(self):
        self.logger.info("Connecting to stream at %r.", self.parameters.http_url)

        try:
            req = self.session.get(url=self.parameters.http_url,
                                   stream=True)
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
