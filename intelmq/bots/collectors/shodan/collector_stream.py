# -*- coding: utf-8 -*-
"""
Parameters:
* api_key: The API key

Selectors:
The only possible selector is currently the country:
* countries: A list of strings or a comma separated list with country codes
"""
import pkg_resources

from intelmq.lib.bot import CollectorBot

try:
    import shodan
except ImportError:
    shodan = None


class ShodanStreamCollectorBot(CollectorBot):
    def init(self):
        if shodan is None:
            raise ValueError("Library 'shodan' is needed but not installed.")

        self.set_request_parameters()
        if tuple(int(v) for v in pkg_resources.get_distribution("shodan").version.split('.')) <= (1, 8, 1):
            if self.proxy:
                raise ValueError('Proxies are given but shodan-python > 1.8.1 is needed for proxy support.')
            else:
                self.api = shodan.Shodan(self.parameters.api_key)
        else:
            self.api = shodan.Shodan(self.parameters.api_key,
                                     proxies=self.proxy)
        if isinstance(self.parameters.countries, str):
            self.countries = self.parameters.countries.split(',')

    def process(self):
        for line in self.api.stream.countries(timeout=self.http_timeout_sec, raw=True,
                                              countries=self.countries):
            report = self.new_report()
            report.add('raw', line)
            self.send_message(report)


BOT = ShodanStreamCollectorBot
