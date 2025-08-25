"""
SPDX-FileCopyrightText: 2025 Institute for Common Good Technology & Malawi CERT
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from pkg_resources import get_distribution
from json import dumps as json_dumps
from typing import Optional

from intelmq.lib.bot import CollectorBot

try:
    from shodan import Shodan
except ImportError:
    Shodan = None


class ShodanAlertCollectorBot(CollectorBot):
    """
    Stream Listener for Shodan Alerts
    """

    api_key: str = None
    # Shodan only uses HTTPS, so it's fine to only offer the HTTPS proxy parameter, not also the HTTPS proxy
    https_proxy: Optional[str] = None

    def init(self):
        if Shodan is None:
            raise ValueError("Library 'shodan' is needed but not installed.")

        self.proxy = ({'http': self.https_proxy,  # just for safety, also add the proxy for http, although it should never be in use
                       'https': self.https_proxy}
                      if self.https_proxy
                      else {})
        if tuple(int(v) for v in get_distribution("shodan").version.split('.')) <= (1, 8, 1):
            if self.proxy:
                raise ValueError('Proxies are given but shodan-python > 1.8.1 is needed for proxy support.')
            else:
                self.api = Shodan(self.api_key)
        else:
            self.api = Shodan(self.api_key,
                              proxies=self.proxy)

    def process(self):
        for alert in self.api.stream.alert():
            report = self.new_report()
            report['raw'] = json_dumps(alert)
            self.send_message(report)

    @staticmethod
    def check(parameters: dict) -> Optional[list[list[str]]]:
        messages = []
        if 'api_key' not in parameters or not parameters['api_key']:
            messages.append(["error", "Parameter 'api_key' not given."])

        if not Shodan:
            if 'https_proxy' in parameters:
                messages.append(["error", "Library 'shodan' is needed but not installed. Required version: At least 1.8.1 for HTTPS Proxy support."])
            else:
                messages.append(["error", "Library 'shodan' is needed but not installed."])
        else:
            shodan_version = tuple(int(v) for v in get_distribution("shodan").version.split('.'))
            if 'https_proxy' in parameters and shodan_version <= (1, 8, 1):
                messages.append(["error", "Library 'shodan' needs to be updated. At least version 1.8.1 is required for HTTPS Proxy support."])

        return messages


BOT = ShodanAlertCollectorBot
