# -*- coding: utf-8 -*-
"""
IDEA classification: https://idea.cesnet.cz/en/classifications
"""
from collections import Sequence, Mapping
from base64 import b64decode
from uuid import uuid4
from urllib.parse import quote_plus

from intelmq.lib.bot import Bot


def quot(s):
    return quote_plus(s or "")


def addr4(s):
    return s if ":" not in s else None


def addr6(s):
    return s if ":" in s else None


class IdeaExpertBot(Bot):

    type_to_category = {
        "phishing": "Fraud.Phishing",
        "ddos": "Availability.DDoS",
        "spam": "Abusive.Spam",
        "scanner": "Recon.Scanning",
        "dropzone": "Information.UnauthorizedAccess",
        "infected system": "Malware",
        "malware configuration": "Malware",
        "botnet drone": "Malware",
        "ransomware": "Malware",
        "malware": "Malware",
        "c&c": "Intrusion.Botnet",
        "exploit": "Attempt.Exploit",
        "brute-force": "Attempt.Login",
        "ids alert": "Attempt.Exploit",
        "defacement": "Intrusion.AppCompromise",
        "compromised": "Intrusion.AdminCompromise",
        "backdoor": "Intrusion.AdminCompromise",
        "vulnerable service": "Vulnerable.Open",
        "vulnerable client": "Vulnerable.Config",
        "blacklist": "Other",
        "dga domain": "Anomaly.Behaviour",
        "proxy": "Vulnerable.Config",
        "leak": "Information",
        "tor": "Other",
        "other": "Other",
        "unknown": "Other",
        "test": "Test",
        "unauthorized-command": "Intrusion.AdminCompromise",
        "unauthorized-login": "Intrusion.AdminCompromise",
        "violence": "Abusive.Violence",
        "data-loss": "Information",
        "burglary": "Intrusion",
        "weak-crypto": "Vulnerable.Config",
        "Unauthorised-information-access": "Information.UnauthorizedAccess",
        "privileged-account-compromise": "Intrusion.AdminCompromise",
        "potentially-unwanted-accessible": "Vulnerable.Open",
        "application-compromise": "Intrusion.AppCompromise",
        "unauthorized-use-of-resources": "Fraud.UnauthorizedUsage",
        "masquerade": "Fraud.Scam",
        "harmful-speech": "Abusive.Harassment",
        "unprivileged-account-compromise": "Intrusion.UserCompromise",
        "social-engineering": "Recon.SocialEngineering",
        "dos": "Availability.DoS",
        "information-disclosure": "Information.UnauthorizedAccess",
        "sniffing": "Recon.Sniffing",
        "vulnerable-system": "Vulnerable.Config",
        "Unauthorised-information-modification": "Information.UnauthorizedModification",
        "sabotage": "Availability.Sabotage",
        "malware-distribution": "Malware",
        "outage": "Availability.Outage",
        "ddos-amplifier": "Intrusion.Botnet",
        "copyright": "Fraud.Copyright",
    }

    type_to_source_type = {
        # Added nonstandard Dropzone, MalwareConf, DGA, will consider adding to Idea spec

        "phishing": "Phishing",
        "dropzone": "Dropzone",
        "malware configuration": "MalwareConf",
        "c&c": "CC",
        "dga domain": "DGA",
        "proxy": "Proxy",
        "tor": "Tor",
        "malware-distribution": "Malware"
    }

    def init(self):
        # Translation initialization is moved to method and called during
        # instantiation, because we need access to self.
        self.translation = {
            # Added nonstandard Source/Target.Type = "Tor" tag; will add to Idea spec
            # Added nonstandard Source/Target.Account, PTR and Local* keys,
            #    will consider incorporating into Idea
            # Deliberately omitted, will consider based on real world data
            # *.geolocation - not directly supported by Idea
            # *.allocated - ditto
            # *.as_name - ditto
            # *.network - ditto
            # *.abuse_contact - ditto
            # *.registry - ditto
            # extra - too informal, will consider based on real world data

            "Format": lambda s: "IDEA0",
            "Description": lambda s: "%s: %s" % (
                s["feed.name"],
                s.get("event_description.text",
                      s.get("comment",
                            s.get("classification.type", "unknown")))
            ),
            "Category": [
                lambda s: self.type_to_category[s.get("classification.type", "unknown")],
                lambda s: "Test" if self.parameters.test_mode else None
            ],
            "DetectTime": "time.observation",
            "EventTime": "time.source",
            "ID": lambda s: str(uuid4()),
            "RelID": lambda s: "hash:" + quot(s["event_hash"]),
            "Confidence": lambda s: min(1, max(0, s["feed.accuracy"] / 100)),
            "Note": "comment",
            "Ref": [
                lambda s: "malid:" + quot(s["classification.identifier"]),
                "event_description.url",
                lambda s: "intelmq_feed:" + quot(s["feed.code"]),
                lambda s: "misp_attr:" + quot(s["misp.attribute_uuid"]),
                lambda s: "misp_event:" + quot(s["misp.event_uuid"]),
                lambda s: "rtir:" + quot(s["rtir_id"]),
                "screenshot_url"
            ],
            "Attach": [
                {
                    "Hash": [
                        lambda s: "crypt:" + quot(s["malware.hash"]),
                        lambda s: "md5:" + quot(s["malware.hash.md5"]),
                        lambda s: "sha1:" + quot(s["malware.hash.sha1"])
                    ],
                    "Ref": [lambda s: "malware:" + "-".join((quot(s["malware.name"]), quot(s.get("malware.version", ""))))]
                },
                {
                    "Content": lambda s: b64decode(s["raw"]).decode("ISO-8859-1"),
                    "Type": [lambda s: s["raw"] and "OrigData"],
                    "Ref": ["feed.url"]
                }
            ],
            "Source": [
                {
                    "Proto": ["protocol.transport", "protocol.application"],
                    "Type": [
                        lambda s: self.type_to_source_type.get(s["classification.type"], None),
                        lambda s: s["source.tor_node"] and "Tor"
                    ],
                    "Account": ["source.account"],
                    "ASN": ["source.asn"],
                    "Hostname": ["source.fqdn"],
                    "IP4": [lambda s: addr4(s["source.ip"])],
                    "IP6": [lambda s: addr6(s["source.ip"])],
                    "LocalHostname": ["source.local_hostname"],
                    "LocalIP4": [lambda s: addr4(s["source.local_ip"])],
                    "LocalIP6": [lambda s: addr6(s["source.local_ip"])],
                    "Port": ["source.port"],
                    "PTR": ["source.reverse_dns"],
                    "URL": ["source.url"],
                    "Note": "status"
                }
            ],
            "Target": [
                {
                    "Proto": ["protocol.transport", "protocol.application"],
                    "Type": [lambda s: s["destination.tor_node"] and "Tor"],
                    "Account": ["destination.account"],
                    "ASN": ["destination.asn"],
                    "Hostname": ["destination.fqdn"],
                    "IP4": [lambda s: addr4(s["destination.ip"])],
                    "IP6": [lambda s: addr6(s["destination.ip"])],
                    "LocalHostname": ["destination.local_hostname"],
                    "LocalIP4": [lambda s: addr4(s["destination.local_ip"])],
                    "LocalIP6": [lambda s: addr6(s["destination.local_ip"])],
                    "Port": ["destination.port"],
                    "PTR": ["destination.reverse_dns"],
                    "URL": ["destination.url"],
                    "Note": "status"
                }
            ]
        }

    def get_value(self, src, value):
        try:
            if callable(value):
                value = value(src)
            elif isinstance(value, str):
                value = src[value]
            elif isinstance(value, Sequence):
                value = self.process_list(src, value)
            elif isinstance(value, Mapping):
                value = self.process_dict(src, value)
        except (KeyError, IndexError):
            # Usually raised when key not present in source Event
            # Other nasty exceptions will get catched and logged by IMQ machinery
            value = None
        return value

    def process_list(self, src, description):
        target = []
        for desc in description:
            val = self.get_value(src, desc)
            if val is not None:
                target.append(val)
        return target or None

    def process_dict(self, src, description):
        target = {}
        for key, desc in description.items():
            val = self.get_value(src, desc)
            if val is not None:
                target[key] = val
        return target or None

    def process(self):
        event = self.receive_message()
        idea_dict = self.process_dict(event, self.translation)
        event.add("output", idea_dict)
        self.send_message(event)
        self.acknowledge_message()


BOT = IdeaExpertBot
