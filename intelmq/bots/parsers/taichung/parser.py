# -*- coding: utf-8 -*-

import re

from intelmq.lib import utils
from intelmq.lib.bot import Bot

CLASSIFICATION = {
    "brute-force": ["brute-force", "brute force", "mysql"],
    "c&c": ["c&c server"],
    "botnet drone": ["irc-botnet"],
    "malware": ["malware provider", "malware website", '\u60e1\u610f', "worm"],
    "scanner": ["scan"],
    "exploit": ["bash", "php-cgi", "phpmyadmin"],
}


class TaichungCityNetflowParserBot(Bot):

    def get_type(self, value):
        value = value.lower()
        for event_type, keywords in CLASSIFICATION.items():
            for keyword in keywords:
                if keyword in value:
                    return event_type
        return "unknown"

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.split('<tr>'):

            # Get IP and Type
            info1 = re.search(
                ">[\ ]*(\d+\.\d+\.\d+\.\d+)[\ ]*<.*</td><td>([^<]+)</td>", row)

            if not info1:
                continue

            # Get Timestamp
            info2 = re.search(
                "<td>[\ ]*(\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2})[\ ]*</td>",
                row)

            event = self.new_event(report)

            description = info1.group(2)
            description = utils.decode(description)
            event_type = self.get_type(description)
            time_source = info2.group(1) + " UTC-8"

            event.add("time.source", time_source)
            event.add("source.ip", info1.group(1))
            event.add('classification.type', event_type)
            event.add('event_description.text', description)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = TaichungCityNetflowParserBot
