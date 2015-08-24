# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Event

REGEX_IP = "^[^ \t]+"
REGEX_TIMESTAMP = "# ([^ \t]+ [^ \t]+)"


class BruteForceBlockerParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):

            if row.startswith('#'):
                continue

            event = Event()

            match = re.search(REGEX_IP, row)
            if match:
                ip = match.group()

            match = re.search(REGEX_TIMESTAMP, row)
            if match:
                timestamp = match.group(1) + " UTC"

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('time.source', timestamp, sanitize=True)
            event.add('source.ip', ip, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('classification.type', u'brute-force')

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = BruteForceBlockerParserBot(sys.argv[1])
    bot.start()
