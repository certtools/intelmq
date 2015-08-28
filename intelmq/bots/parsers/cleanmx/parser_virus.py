# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import io
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress
from intelmq.lib.message import Event

COLUMNS = {
    "line": "__IGNORE__",
    "id": "__IGNORE__",
    "sub": "__IGNORE__",
    "firsttime": "time.source",
    "lasttime": "__IGNORE__",
    "scanner": "__IGNORE__",
    "virusname": "malware.name",
    "url": "source.url",
    "recent": "__IGNORE__",
    "response": "__IGNORE__",
    "ip": "source.ip",
    "as": "source.asn",
    "review": "__IGNORE__",
    "domain": "source.fqdn",
    "country": "source.geolocation.cc",
    "source": "__IGNORE__",
    "email": "source.abuse_contact",
    "inetnum": "__IGNORE__",
    "netname": "__IGNORE__",
    "ddescr": "__IGNORE__",
    "ns1": "__IGNORE__",
    "ns2": "__IGNORE__",
    "ns3": "__IGNORE__",
    "ns4": "__IGNORE__",
    "ns5": "__IGNORE__"
}


class CleanMXVirusParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))

        fp = io.StringIO(raw_report)
        rows = csv.DictReader(fp)

        for row in rows:
            event = Event()

            for key, value in row.items():
                if not value:
                    continue

                key = COLUMNS[key]

                if key is "__IGNORE__" or key is "__TDB__":
                    continue

                if key == "source.fqdn" and IPAddress.is_valid(value,
                                                               sanitize=True):
                    continue

                if key == "time.source":
                    value = value + " UTC"

                if key == "source.asn" and value.startswith("ASNA"):
                    continue

                if key == "source.asn":
                    for asn in value.split(','):
                        if asn.startswith("AS"):
                            value = asn.split("AS")[1]
                            break

                event.add(key, value, sanitize=True)

            event.add('time.observation', report.value(
                'time.observation'), sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('classification.type', u'malware')
            event.add("raw", ",".join(row), sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = CleanMXVirusParserBot(sys.argv[1])
    bot.start()
