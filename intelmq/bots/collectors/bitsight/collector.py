# -*- coding: utf-8 -*-

import sys

import pycurl
from intelmq.lib.bot import Bot
from intelmq.lib.message import Report


class BitsightCollectorBot(Bot):

    def init(self):
        self.logger.info("Connecting to BitSightTech stream server") 
        http_proxy = getattr(self.parameters, http_proxy, None) 
        api_key = getattr(self.parameters, api_key)
        http_url = getattr(self.parameters, http_url) 
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.PROXY, http_proxy)
        self.conn.setopt(pycurl.URL, str(http_url+api_key))
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)

    def process(self):
        self.conn.perform()

    def on_receive(self, data):
        for line in data.decode().splitlines():
            line = line.strip()
            if line == "":
                continue

            report = Report()
            report.add("raw", str(line))
            report.add("feed.name", self.parameters.feed)
            report.add("feed.accuracy", self.parameters.accuracy)
            self.send_message(report)


if __name__ == "__main__":
    bot = BitsightCollectorBot(sys.argv[1])
    bot.start()
