# -*- coding: utf-8 -*-
import json

from intelmq.lib.bot import CollectorBot

try:
    from OTXv2 import OTXv2
except ImportError:
    OTXv2 = None


class AlienVaultOTXCollectorBot(CollectorBot):

    def init(self):
        if OTXv2 is None:
            raise ValueError('Could not import OTXv2. Please install it.')

        if hasattr(self.parameters, 'http_ssl_proxy'):
            self.logger.warning("Parameter 'http_ssl_proxy' is deprecated and will be removed in "
                                "version 1.0!")
            if not self.parameters.https_proxy:
                self.parameters.https_proxy = self.parameters.http_ssl_proxy

    def process(self):
        self.logger.info("Downloading report through API")
        otx = OTXv2(self.parameters.api_key, proxy=self.parameters.https_proxy)
        pulses = otx.getall()
        self.logger.info("Report downloaded.")

        report = self.new_report()
        report.add("raw", json.dumps(pulses))
        self.send_message(report)


BOT = AlienVaultOTXCollectorBot
