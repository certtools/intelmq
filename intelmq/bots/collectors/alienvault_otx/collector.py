# -*- coding: utf-8 -*-
import json
import sys

from intelmq.lib.bot import CollectorBot
from intelmq.lib.message import Report

from .OTXv2 import OTXv2


class AlienVaultOTXCollectorBot(CollectorBot):

    def process(self):
        self.logger.info("Downloading report through API")
        https_proxy = getattr(self.parameters, 'http_ssl_proxy', None)
        otx = OTXv2(self.parameters.api_key, proxy=https_proxy)
        pulses = otx.getall()
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", json.dumps(pulses))
        self.send_message(report)


if __name__ == "__main__":
    bot = AlienVaultOTXCollectorBot(sys.argv[1])
    bot.start()
