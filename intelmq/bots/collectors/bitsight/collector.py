# -*- coding: utf-8 -*-

import re
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report

import pycurl


class BitsightCollectorBot(Bot):

    def init(self):
        self.logger.info("Connecting to BitSightTech stream server")
        http_proxy = self.parameters.http_proxy
        https_proxy = self.parameters.http_ssl_proxy
        self.conn  = pycurl.Curl()
        if http_proxy:
            self.conn.setopt(pycurl.PROXY, str(http_proxy))
        if https_proxy:
            self.conn.setopt(pycurl.PROXY, str(https_proxy))
        self.conn.setopt(pycurl.URL, str(self.parameters.http_url))
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)

    def process(self):
        try:                     # hugly hack, when bot executes self.stop() pycurl raises an exception that makes the bot restart again.
            self.conn.perform()
        except pycurl.error as e:
            if e.args[0] == 23:  # Failed writing body, code 23, we want to catch only this.
                self.logger.info('Shutting down pycurl gracefully')
                self.conn.close()
                self.stop()
            else:
                raise            # and raise everything else, eg: timouts.

    def on_receive(self, data):
        for line in data.decode().splitlines():
            line = line.strip()
            if line == "":
                continue

            report = Report()
            report.add("raw", line)
            report.add("feed.name", self.parameters.feed)
            report.add("feed.accuracy", self.parameters.accuracy)
            report.add("feed.url", self.parameters.http_url)

            self.send_message(report)

if __name__ == "__main__":
    bot = BitsightCollectorBot(sys.argv[1])
    bot.start()
