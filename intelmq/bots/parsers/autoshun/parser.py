# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import ClassificationType
from intelmq.lib.message import Event

TAXONOMY = {
    "brute force": "brute-force",
    "bruteforce": "brute-force",
    "scan": "scanner",
    "cve": "exploit",
    "sql inject": "exploit",
}


class AutoshunParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))
        raw_report_splitted = raw_report.split("</tr>")[2:]

        parser = HTMLParser()

        for row in raw_report_splitted:
            event = Event(report)

            row = row.strip()

            if len(row) <= 0:
                continue

            info = row.split("<td>")
            if len(info) < 3:
                continue

            ip = info[1].split('</td>')[0].strip()
            last_seen = info[2].split('</td>')[0].strip() + '-05:00'
            description = parser.unescape(info[3].split('</td>')[0].strip())

            for key in ClassificationType.allowed_values:
                if description.lower().find(key.lower()) > -1:
                    event.add("classification.type", key)
                    break
            else:
                for key, value in TAXONOMY.items():
                    if description.lower().find(key.lower()) > -1:
                        event.add("classification.type", value)
                        break

            if not event.contains("classification.type"):
                event.add("classification.type", u'unknown')

            event.add("time.source", last_seen)
            event.add("source.ip", ip)
            event.add("event_description.text", description)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AutoshunParserBot(sys.argv[1])
    bot.start()
