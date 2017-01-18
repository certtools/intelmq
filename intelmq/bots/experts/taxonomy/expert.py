# -*- coding: utf-8 -*-

from intelmq.lib.bot import Bot

# FIXME: this dict should be on a sparated file

TAXONOMY = {
    # type       # taxonomy
    "phishing": "fraud",
    "proxy": "Other",
    "ddos": "availability",
    "spam": "abusive content",
    "scanner": "information gathering",
    "dropzone": "information content security",
    "malware": "malicious code",
    "botnet drone": "malicious code",
    "ransomware": "malicious code",
    "dga domain": "malicious code",
    "malware configuration": "malicious code",
    "c&c": "malicious code",
    "exploit": "intrusion attempts",
    "brute-force": "intrusion attempts",
    "ids alert": "intrusion attempts",
    "defacement": "intrusions",
    "compromised": "intrusions",
    "backdoor": "intrusions",
    "vulnerable service": "vulnerable",
    "blacklist": "other",
    "unknown": "other",
    "test": "test",
    "other": "other"
}


class TaxonomyExpertBot(Bot):

    def process(self):
        event = self.receive_message()

        if "classification.taxonomy" not in event and "classification.type" in event:
            # set the taxonomy based on the mapping above
            event_type = event.get("classification.type")
            taxonomy = TAXONOMY.get(event_type, 'other')
            event.add("classification.taxonomy", taxonomy)
        elif "classification.taxonomy" not in event and "classification.type" not in event:
            event.add("classification.taxonomy", 'other')
            event.add("classification.type", 'unknown')
        elif "classification.taxonomy" in event and "classification.type" not in event:
            event.add("classification.type", 'unknown')
        else:
            # classifcation given, type given... don't change it
            pass

        self.send_message(event)
        self.acknowledge_message()


BOT = TaxonomyExpertBot
