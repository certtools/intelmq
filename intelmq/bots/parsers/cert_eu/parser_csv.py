# SPDX-FileCopyrightText: 2018 Pierre Dumont
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
CERT-EU parser

"city",  # empty
"source location",  # just a combination of long and lat
"country",  # empty
"as name",  # empty

reported cc, reported as name: ignored intentionally
"""
from collections import defaultdict

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime


class CertEUCSVParserBot(ParserBot):
    """Parse CSV data of the CERT-EU feed"""

    ABUSE_TO_INTELMQ = defaultdict(lambda: "other", {
        "backdoor": "system-compromise",
        "blacklist": "blacklist",
        "botnet drone": "infected-system",
        "brute-force": "brute-force",
        "c2server": "c2-server",
        "compromised server": "system-compromise",
        "ddos infrastructure": "ddos",
        "ddos target": "ddos",
        "defacement": "unauthorised-information-modification",
        "dropzone": "other",
        "exploit url": "exploit",
        "ids alert": "ids-alert",
        "malware-configuration": "malware-configuration",
        "malware url": "malware-distribution",
        "phishing": "phishing",
        "ransomware": "infected-system",
        "scanner": "scanner",
        "spam infrastructure": "spam",
        "test": "test",
        "vulnerable service": "vulnerable-system"
    })

    _unknown_fields = ["threat type", "ns1", "ns2", "response", "recent"]
    _ignore_lines_starting = ["#"]

    def parse_line(self, line, report):
        event = self.new_event(report)
        if line["version"] not in ("1.5", ''):
            raise ValueError("Unknown version %r. Please report this with an example."
                             "" % line["version"])
        for unknown in self._unknown_fields:
            if line[unknown]:
                raise ValueError("Unable to parse field %r. Please report this with an example"
                                 "" % unknown)

        event["extra.datasource"] = line["feed code"]
        event.add("source.ip", line["source ip"])
        event.add("source.network", line["source bgp prefix"])
        event.add("extra.cert_eu_time_observation",
                  DateTime.sanitize(line["observation time"]))
        event.add("tlp", line["tlp"])
        event.add("event_description.text", line["description"])
        event.add("classification.type", self.ABUSE_TO_INTELMQ[line["type"]])
        if line['type'] == 'dropzone':
            event.add("classification.identifier", 'dropzone')
        if line["count"]:
            event["extra.count"] = int(line["count"])
        event.add("time.source", line["source time"])
        event.add("source.geolocation.country", line["source country"])
        event.add("protocol.application", line["protocol"])
        event.add("destination.port", line["destination port"])
        event.add("source.geolocation.latitude", line["source latitude"])
        event.add("source.geolocation.city", line["source city"])
        event.add("source.geolocation.geoip_cc", line["source cc"])
        event.add("source.geolocation.longitude", line["source longitude"])
        event.add("extra.source.geolocation.geohash", line["source geohash"])
        event["extra.first_seen"] = line["first seen"]
        event.add('feed.accuracy',
                  event.get('feed.accuracy', 100) * int(line["confidence level"]) / 100,
                  overwrite=True)
        event["extra.last_seen"] = line["last seen"]
        event["extra.expiration_date"] = line["expiration date"]
        if line["status"]:
            event["status"] = line["status"]
        event.add("event_description.target", line["target"])
        event.add("source.url", line["url"])
        event.add("source.abuse_contact", line["abuse contact"])
        event.add("source.asn", line["source asn"])
        event.add("source.as_name", line["source as name"])
        event.add("source.fqdn", line["domain name"])

        event.add("raw", self.recover_line(line))
        yield event

    parse = ParserBot.parse_csv_dict
    recover_line = ParserBot.recover_line_csv_dict


BOT = CertEUCSVParserBot
