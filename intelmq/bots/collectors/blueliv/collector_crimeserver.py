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
    def init(self):
        if BluelivAPI is None:
            raise MissingDependencyError("sdk.blueliv_api.BluelivAPI")

        if not hasattr(self.parameters, 'api_url'):
            setattr(self.parameters, 'api_url', 'https://freeapi.blueliv.com')

    def process(self):
        self.logger.debug("Downloading report through API.")
        proxy = None
        if self.parameters.http_proxy and self.parameters.https_proxy:
            proxy = {'http': self.parameters.http_proxy,
                     'https': self.parameters.https_proxy}
        api = BluelivAPI(base_url=self.parameters.api_url,
                         token=self.parameters.api_key,
                         log_level=logging.INFO,
                         proxy=proxy)

        response = api.crime_servers.online()
        self.logger.info("Report downloaded.")

        report = self.new_report()
        report.add("raw", json.dumps([item for item in response.items]))
        self.send_message(report)


BOT = BluelivCrimeserverCollectorBot
