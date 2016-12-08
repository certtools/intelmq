# -*- coding: utf-8 -*-
import csv
import io

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress

COLUMNS = {
    "line": "__IGNORE__",
    "id": "__IGNORE__",
    "firsttime": "time.source",
    "lasttime": "__IGNORE__",
    "phishtank": "__IGNORE__",
    "virusname": "malware.name",
    "url": "source.url",
    "recent": "__IGNORE__",
    "response": "__IGNORE__",
    "ip": "source.ip",
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


class CleanMXPhishingParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in csv.DictReader(io.StringIO(raw_report)):
            event = self.new_event(report)

            for key, value in row.items():
                if not value:
                    continue

                if key is None:
                    self.logger.warning('Value without key found, skipping the'
                                        ' value: {!r}'.format(value))
                    continue

                key = COLUMNS[key]

                if key == "__IGNORE__" or key == "__TDB__":
                    continue

                if key == "source.fqdn" and IPAddress.is_valid(value,
                                                               sanitize=True):
                    continue

                if key == "time.source":
                    value = value + " UTC"

                event.add(key, value)

            event.add('classification.type', 'phishing')
            event.add("raw", ",".join(row))

            self.send_message(event)
        self.acknowledge_message()


BOT = CleanMXPhishingParserBot
