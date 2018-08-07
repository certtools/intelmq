"""
CERT-EU parser
"""
from intelmq.lib.bot import ParserBot


class CertEUCSVParserBot(ParserBot):

    abuse_to_intelmq = {
        "backdoor": "backdoor",
        "blacklist": "blacklist",
        "botnet drone": "botnet drone",
        "brute-force": "brute-force",
        "c&c": "c&c",
        "compromised server": "compromised",
        "ddos infrastructure": "ddos",
        "ddos target": "--",
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
        "vulnerable service": "vulnerable service",
        "--": "unknown"
    }

    csv_fieldnames = [
        "datasource", "source ip", "observation time", "tlp", "description",
        "type", "count", "source time", "source country", "protocol",
        "destination port", "source latitude", "source city", "source cc",
        "source longitude", "first_seen", "num_sensors", "confidence level",
        "last_seen", "target", "phishing", "asn", "domain name"]
    ignore_lines_starting = ["#"]

    def parse_line(self, line, report):
        event = self.new_event(report)
        # event["?"] = line["datasource"]
        event["source.ip"] = line["source ip"]
        event["time.observation"] = line["observation time"]
        event["tlp"] = line["tlp"]
        event["event_description.text"] = line["description"]  # TBC
        event["classification.type"] = self.abuse_to_intelmq.get(
            line["type"], "unknown"
        )
        # event["?"] = line["count"]
        event["time.source"] = line["source time"]
        event["source.geolocation.country"] = line["source country"]
        event["protocol.application"] = line["protocol"]
        event["destination.port"] = line["destination port"]
        event["source.geolocation.latitude"] = line["source latitude"]
        event["source.geolocation.city"] = line["source city"]
        event["source.geolocation.geoip_cc"] = line["source cc"]
        event["source.geolocation.longitude"] = line["source longitude"]
        # event["?"] = line["first_seen"]
        # event["?"] = line["num_sensors"]
        event["feed.accuracy"] = line["confidence level"]  # TBC is 0<=x<=100 ?
        # event["?"] = line["last seen"]
        event["event_description.target"] = line["target"]  # TBC
        event["source.url"] = line["phishing"]  # TBC or destination.url?
        event["source.asn"] = line["asn"]  # TBC or destination?
        event["source.fqdn"] = line["domain name"]  # TBC or destination?

        event["raw"] = self.recover_line(line)
        yield event

    parse = ParserBot.parse_csv_dict
    recover_line = ParserBot.recover_line_csv_dict


BOT = CertEUCSVParserBot
