# SPDX-FileCopyrightText: 2015 robcza
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json
import logging

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from sdk.blueliv_api import BluelivAPI
except ImportError:
    BluelivAPI = None


class BluelivCrimeserverCollectorBot(CollectorBot):
    """Collect reports from the Blueliv Crimeserver API"""
    api_key: str = "<insert your api key>"
    api_url: str = "https://freeapi.blueliv.com"
    rate_limit: int = 3600

    def init(self):
        if BluelivAPI is None:
            raise MissingDependencyError("sdk.blueliv_api.BluelivAPI")

    def process(self):
        self.logger.debug("Downloading report through API.")
        proxy = None
        if self.http_proxy and self.https_proxy:
            proxy = {'http': self.http_proxy,
                     'https': self.https_proxy}
        api = BluelivAPI(base_url=self.api_url,
                         token=self.api_key,
                         log_level=logging.INFO,
                         proxy=proxy)

        response = api.crime_servers.online()
        self.logger.info("Report downloaded.")

        report = self.new_report()
        report.add("raw", json.dumps([item for item in response.items]))
        self.send_message(report)


BOT = BluelivCrimeserverCollectorBot
