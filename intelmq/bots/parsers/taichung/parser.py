# -*- coding: utf-8 -*-
"""
unmapped:
    : bing says "Over-the-line",
"""
import re
import warnings

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot

CLASSIFICATION = {
    "brute-force": ["brute-force", "brute force", "mysql",
                    "mssql 密碼猜測攻擊",  # Password Guess Attack
                    "office 365 attack", "sip attack", "ssh attack",
                    "ssh密碼猜測攻擊",  # Password Guess Attack
                    ],
    "c2server": ["c&c server", "attack controller"],
    "infected-system": ["irc-botnet"],
    "malware": ["malware provider", "malware website", '\u60e1\u610f', "worm", "malware proxy"],
    "scanner": ["scan"],
    "exploit": ["bash", "php-cgi", "phpmyadmin"],
    "ddos": ["ddos"],
    "application-compromise": ["injection"],  # apache vulns, sql
    "ids-alert": ["backdoor"],  # ids-alert is exploitation of known vulnerability
    "dos": ["dns", "dos",  # must be after ddos
            "超量連線",  # google: "Excess connection"
            ],
}


class TaichungNetflowRecentParserBot(ParserBot):

    def get_type(self, value):
        value = value.lower()
        for event_type, keywords in CLASSIFICATION.items():
            for keyword in keywords:
                if keyword in value:
                    return event_type
        warnings.warn("Unknown classification: %r. Please report this as bug."
                      "" % value)
        return "unknown"

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.split('<tr>'):
            yield row

    def parse_line(self, row, report):
        # Get IP Address and Type
        info1 = re.search(
            r">[\ ]*(\d+\.\d+\.\d+\.\d+)[\ ]*<.*</td><td>([^<]+)</td>", row)

        if not info1:
            return  # abort if no IP address found

        # Get Timestamp
        info2 = re.search(
            r"<td>[\ ]*(\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2})[\ ]*</td>",
            row)
        cc_search = re.search(r'([a-z]+).gif"', row)

        event = self.new_event(report)

        description = info1.group(2)
        event_type = self.get_type(description)  # without decoding here, b/c of the unicode signs
        description = utils.decode(description)
        time_source = info2.group(1) + " UTC-8"

        event.add("time.source", time_source)
        event.add("source.ip", info1.group(1))
        event.add('classification.type', event_type)
        event.add('event_description.text', description)
        if cc_search:
            event.add('source.geolocation.cc', cc_search.group(1))
        event.add("raw", row)

        yield event


BOT = TaichungNetflowRecentParserBot
