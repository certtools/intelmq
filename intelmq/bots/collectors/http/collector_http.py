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
import sys

from intelmq.bots.collectors.http.lib import fetch_url
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


class URLCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report from %s" % self.parameters.url)

        http_header = getattr(self.parameters, 'http_header', {})
        verify_cert = getattr(self.parameters, 'verify_cert', True)

        if hasattr(self.parameters, 'username') and hasattr(self.parameters,
                                                            'password'):
            auth = (self.parameters.username, self.parameters.password)
        else:
            auth = None

        raw_report = fetch_url(self.parameters.url,
                               timeout=60.0,
                               http_proxy=self.parameters.http_proxy,
                               https_proxy=self.parameters.https_proxy,
                               user_agent=self.parameters.http_user_agent,
                               header=http_header,
                               verify_cert=verify_cert,
                               auth=auth,
                               )
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", raw_report, sanitize=True)
        report.add("feed.name", self.parameters.feed, sanitize=True)
        report.add("feed.url", self.parameters.url, sanitize=True)
        time_observation = DateTime().generate_datetime_now()
        report.add('time.observation', time_observation, sanitize=True)
        self.send_message(report)


if __name__ == "__main__":
    bot = URLCollectorBot(sys.argv[1])
    bot.start()
