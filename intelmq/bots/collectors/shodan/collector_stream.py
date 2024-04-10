# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Parameters:
* api_key: The API key

Selectors:
* countries: A list of strings or a comma separated list with country codes
* alert: An alert ID from monitor.shodan.io
"""
import pkg_resources
from http.client import IncompleteRead
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from requests.exceptions import ChunkedEncodingError, ConnectionError
from typing import List, Optional

from intelmq.lib.bot import CollectorBot

try:
    import shodan
    from shodan.exception import APIError
except ImportError:
    shodan = None


class ShodanStreamCollectorBot(CollectorBot):
    "Collect the Shodan stream from the Shodan API"
    api_key: str = "<INSERT your API key>"
    countries: List[str] = []
    alert: Optional[str] = None

    def init(self):
        if shodan is None:
            raise ValueError("Library 'shodan' is needed but not installed.")

        self.set_request_parameters()
        if tuple(int(v) for v in pkg_resources.get_distribution("shodan").version.split('.')) <= (1, 8, 1):
            if self.proxy:
                raise ValueError('Proxies are given but shodan-python > 1.8.1 is needed for proxy support.')
            else:
                self.api = shodan.Shodan(self.api_key)
        else:
            self.api = shodan.Shodan(self.api_key,
                                     proxies=self.proxy)
        if isinstance(self.countries, str):
            if self.countries and self.alert:
                raise ValueError('Both alert and country filters specified. Please use only one selector.')
            self.countries = self.countries.split(',')

        self.__error_count = 0

    def process(self):
        try:
            if self.alert:
                stream = self.api.stream.alert(
                    aid=self.alert,
                    timeout=self.http_timeout_sec,
                    raw=True,
                )
            else:
                stream = self.api.stream.countries(
                    countries=self.countries,
                    timeout=self.http_timeout_sec,
                    raw=True,
                )

            for line in stream:
                report = self.new_report()
                report.add('raw', line)
                self.send_message(report)
                self.__error_count = 0
        except (ChunkedEncodingError,
                ConnectionError,
                ProtocolError,
                IncompleteRead,
                ReadTimeoutError,
                APIError) as exc:
            self.__error_count += 1
            if (self.__error_count > self.error_max_retries):
                self.__error_count = 0
                raise
            else:
                self.logger.info('Got exception %r, retrying (consecutive error count %d <= %d).',
                                 exc, self.__error_count, self.error_max_retries)


BOT = ShodanStreamCollectorBot
