# SPDX-FileCopyrightText: 2015 robcza
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
    "Collect reports from the AlienVault OTX Collector API. Report varies according to subscriptions."
    api_key: str = "<insert your api key>"
    interval: int = 24
    modified_pulses_only: bool = False
    rate_limit: int = 3600

    def init(self):
        if OTXv2 is None:
            raise MissingDependencyError("OTXv2")

        self.modified_pulses_only = False
        if hasattr(self, 'modified_pulses_only'):
            self.modified_pulses_only = self.modified_pulses_only

    def process(self):
        self.logger.info("Downloading report through API.")
        otx = OTXv2(self.api_key, proxy=self.https_proxy)
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
