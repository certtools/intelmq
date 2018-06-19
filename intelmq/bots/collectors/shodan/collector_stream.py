# -*- coding: utf-8 -*-
"""
Parameter:
* api_key: The API key
"""
import shodan

from intelmq.lib.bot import CollectorBot

URL_LIST = 'https://interflow.azure-api.net/file/api/file/listsharedfiles'
URL_DOWNLOAD = 'https://interflow.azure-api.net/file/api/file/download?fileName=%s'


class ShodanStreamCollectorBot(CollectorBot):
    def init(self):
        self.set_request_parameters()
        self.api = shodan.Shodan(self.parameters.api_key)

    def process(self):
        for line in self.api.stream.countries(timeout=self.http_timeout_sec, raw=True, countries=self.parameters.countries):
            report = self.new_report()
            report.add('raw', line)
#                             proxies=self.proxy,
#                             verify=self.http_verify_cert,
            self.send_message(report)


BOT = ShodanStreamCollectorBot
