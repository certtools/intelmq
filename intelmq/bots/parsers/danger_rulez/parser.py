# -*- coding: utf-8 -*-
import re

from intelmq.lib import utils
from intelmq.lib.bot import Bot

REGEX_IP = "^[^ \t]+"
REGEX_TIMESTAMP = "# ([^ \t]+ [^ \t]+)"


class BruteForceBlockerParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.splitlines():

            if not row or row.startswith('#'):
                continue

            event = self.new_event(report)

            match = re.search(REGEX_IP, row)
            ip = None
            if match:
                ip = match.group()

            match = re.search(REGEX_TIMESTAMP, row)
            timestamp = None
            if match:
                timestamp = match.group(1) + " UTC"

            if not timestamp:
                raise ValueError('No timestamp found.')
            elif not ip:
                raise ValueError('No ip found.')

            event.add('time.source', timestamp)
            event.add('source.ip', ip)
            event.add('classification.type', 'brute-force')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = BruteForceBlockerParserBot
