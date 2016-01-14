# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys
from .OTXv2 import OTXv2
import json

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report
from intelmq.lib.harmonization import DateTime


class AlienVaultOTXCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report through API")
        otx = OTXv2(self.parameters.api_key)
        pulses = otx.getall()
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", json.dumps(pulses), sanitize=True)
        report.add("feed.name", self.parameters.feed, sanitize=True)
        report.add("feed.accuracy", self.parameters.accuracy, sanitize=True)
        time_observation = DateTime().generate_datetime_now()
        report.add('time.observation', time_observation, sanitize=True)
        self.send_message(report)


if __name__ == "__main__":
    bot = AlienVaultOTXCollectorBot(sys.argv[1])
    bot.start()
