# -*- coding: utf-8 -*-
import datetime
import json

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from OTXv2 import OTXv2
except ImportError:
    OTXv2 = None


class AlienVaultOTXCollectorBot(CollectorBot):

    def init(self):
        if OTXv2 is None:
            raise MissingDependencyError("OTXv2")

        self.modified_pulses_only = False
        if hasattr(self.parameters, 'modified_pulses_only'):
            self.modified_pulses_only = self.parameters.modified_pulses_only
            self.interval = getattr(self.parameters, 'interval', 24)

    def process(self):
        self.logger.info("Downloading report through API.")
        otx = OTXv2(self.parameters.api_key, proxy=self.parameters.https_proxy)
        if self.modified_pulses_only:
            self.logger.info("Fetching only modified pulses.")
            interval = (datetime.datetime.now() -
                        datetime.timedelta(hours=self.interval)).isoformat()
            pulses = otx.getsince(interval, limit=9999)
        else:
            self.logger.info("Fetching all pulses.")
            pulses = otx.getall()
        self.logger.info("Report downloaded.")

        report = self.new_report()
        report.add("raw", json.dumps(pulses))
        self.send_message(report)


BOT = AlienVaultOTXCollectorBot
