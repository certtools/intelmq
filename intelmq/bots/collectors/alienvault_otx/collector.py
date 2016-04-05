# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys
from .OTXv2 import OTXv2
import json

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report


class AlienVaultOTXCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report through API")
        otx = OTXv2(self.parameters.api_key)
        pulses = otx.getall()
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", json.dumps(pulses))
        report.add("feed.name", self.parameters.feed)
        report.add("feed.accuracy", self.parameters.accuracy)
        self.send_message(report)


if __name__ == "__main__":
    bot = AlienVaultOTXCollectorBot(sys.argv[1])
    bot.start()
