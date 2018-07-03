# -*- coding: utf-8 -*-
import json
import logging

from intelmq.lib.bot import CollectorBot

try:
    from sdk.blueliv_api import BluelivAPI
except ImportError:
    BluelivAPI = None


class BluelivCrimeserverCollectorBot(CollectorBot):
    def init(self):
        if BluelivAPI is None:
            raise ValueError('Could not import sdk.blueliv_api.BluelivAPI. Please install it.')

    def process(self):
        self.logger.debug("Downloading report through API.")
        proxy = None
        if self.parameters.http_proxy and self.parameters.https_proxy:
            proxy = {'http': self.parameters.http_proxy,
                     'https': self.parameters.https_proxy}
        api = BluelivAPI(base_url='https://freeapi.blueliv.com',
                         token=self.parameters.api_key,
                         log_level=logging.INFO,
                         proxy=proxy)

        response = api.crime_servers.online()
        self.logger.info("Report downloaded.")

        report = self.new_report()
        report.add("raw", json.dumps([item for item in response.items]))
        self.send_message(report)


BOT = BluelivCrimeserverCollectorBot
