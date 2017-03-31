# -*- coding: utf-8 -*-

import pycurl
from intelmq.lib.bot import CollectorBot


class BitsightCollectorBot(CollectorBot):

    def init(self):
        if hasattr(self.parameters, 'http_ssl_proxy'):
            self.logger.warning("Parameter 'http_ssl_proxy' is deprecated and will be removed in "
                                "version 1.0!")
            if not self.parameters.https_proxy:
                self.parameters.https_proxy = self.parameters.http_ssl_proxy

        self.logger.info("Connecting to BitSightTech stream server")
        self.conn = pycurl.Curl()
        if self.parameters.http_proxy:
            self.conn.setopt(pycurl.PROXY, self.parameters.http_proxy)
        if self.parameters.https_proxy:
            self.conn.setopt(pycurl.PROXY, self.parameters.https_proxy)
        self.conn.setopt(pycurl.URL, self.parameters.http_url)
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)

    def process(self):
        self.conn.perform()

    def shutdown(self):
        self.conn.close()

    def on_receive(self, data):
        for line in data.decode().splitlines():
            line = line.strip()
            if line == "":
                continue

            report = self.new_report()
            report.add("raw", line)
            report.add("feed.url", self.parameters.http_url)

            self.send_message(report)


BOT = BitsightCollectorBot
