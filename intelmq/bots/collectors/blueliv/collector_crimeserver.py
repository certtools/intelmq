# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from sdk.blueliv_api import BluelivAPI
import json

from intelmq.lib.bot import Bot
from intelmq.lib.message import Report
from intelmq.lib.harmonization import DateTime


class BluelivCrimeserverCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report through API")
        proxy = {'http': '50.60.110.152:80',
                 'https': '50.60.110.152:80'}
        api = BluelivAPI(base_url='https://freeapi.blueliv.com',
                     token=self.parameters.api_key,
                     log_level=logging.INFO,
                     proxy=proxy)

        response = api.crime_servers.online()
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", json.dumps([item for item in response.items]), sanitize=True)
        report.add("feed.name", self.parameters.feed, sanitize=True)
        report.add("feed.accuracy", self.parameters.accuracy, sanitize=True)
        time_observation = DateTime().generate_datetime_now()
        report.add('time.observation', time_observation, sanitize=True)
        self.send_message(report)


if __name__ == "__main__":
    bot = BluelivCrimeserverCollectorBot(sys.argv[1])
    bot.start()
