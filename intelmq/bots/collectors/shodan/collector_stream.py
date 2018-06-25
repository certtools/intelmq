# -*- coding: utf-8 -*-
"""
Parameter:
* api_key: The API key
"""
import shodan

from intelmq.lib.bot import CollectorBot


class ShodanStreamCollectorBot(CollectorBot):
    def init(self):
        self.set_request_parameters()
        self.api = shodan.Shodan(self.parameters.api_key)
        if isinstance(self.parameters.countries, str):
            self.countries = self.parameters.countries.split(',')

    def process(self):
        for line in self.api.stream.countries(timeout=self.http_timeout_sec, raw=True, countries=self.parameters.countries):
            report = self.new_report()
            report.add('raw', line)
#                             proxies=self.proxy,
#                             verify=self.http_verify_cert,
            self.send_message(report)


BOT = ShodanStreamCollectorBot
