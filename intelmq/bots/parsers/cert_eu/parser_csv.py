"""
CERT-EU parser
"""
from intelmq.lib.bot import ParserBot
from collections import defaultdict


class CertEUCSVParserBot(ParserBot):

    abuse_to_intelmq = defaultdict(lambda: "unknown", {
        "backdoor": "backdoor",
        "blacklist": "blacklist",
        "botnet drone": "botnet drone",
        "brute-force": "brute-force",
        "c&c": "c&c",
        "compromised server": "compromised",
        "ddos infrastructure": "ddos",
        "ddos target": "ddos",
        "defacement": "defacement",
        "dropzone": "dropzone",
        "exploit url": "exploit",
        "ids alert": "ids alert",
        "malware configuration": "malware configuration",
        "malware url": "malware",
        "phishing": "phishing",
        "ransomware": "ransomware",
        "scanner": "scanner",
        "spam infrastructure": "spam",
        "test": "test",
        "vulnerable service": "vulnerable service"
    })

    csv_fieldnames = [
        "datasource", "source ip", "observation time", "tlp", "description",
        "type", "count", "source time", "source country", "protocol",
        "destination port", "source latitude", "source city", "source cc",
        "source longitude", "first_seen", "num_sensors", "confidence level",
        "last_seen", "target", "url", "asn", "domain name"]
    ignore_lines_starting = ["#"]

    def parse_line(self, line, report):
        event = self.new_event(report)
        if "datasource" in line:
            event["extra.datasource"] = line["datasource"]
        event.add("source.ip", line["source ip"])
        event.add("time.observation", line["observation time"])
        event.add("tlp", line["tlp"])
        event.add("event_description.text", line["description"])
        event.add("classification.type", self.abuse_to_intelmq[line["type"]])
        if "count" in line:
            event["extra.count"] = int(line["count"]) if line["count"] else None
        event.add("time.source", line["source time"])
        event.add("source.geolocation.country", line["source country"])
        event.add("protocol.application", line["protocol"])
        event.add("destination.port", line["destination port"])
        event.add("source.geolocation.latitude", line["source latitude"])
        event.add("source.geolocation.city", line["source city"])
        event.add("source.geolocation.geoip_cc", line["source cc"])
        event.add("source.geolocation.longitude", line["source longitude"])
        if "first_seen" in line:
            event["extra.first_seen"] = line["first_seen"]
        if "num_sensors" in line:
            event["extra.num_sensors"] = line["num_sensors"]
        event.add("feed.accuracy", line["confidence level"])
        if "last_seen" in line:
            event["extra.last_seen"] = line["last_seen"]
        event.add("event_description.target", line["target"])
        event.add("source.url", line["url"])
        event.add("source.asn", line["asn"])
        event.add("source.fqdn", line["domain name"])

        event.add("raw", self.recover_line(line))
        yield event

    parse = ParserBot.parse_csv_dict
    recover_line = ParserBot.recover_line_csv_dict


BOT = CertEUCSVParserBot
