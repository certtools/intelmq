# -*- coding: utf-8 -*-
"""
The mapping follows
Reference Security Incident Taxonomy Working Group – RSIT WG
https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/
with extensions.
"""

from intelmq.lib.bot import Bot

# FIXME: this dict should be on a separated file

TAXONOMY = {
    # type       # taxonomy
    # sorted!
    "spam": "abusive content",
    "harmful-speech": "abusive-content",
    "violence": "abusive-content",
    "ddos": "availability",
    "dos": "availability",
    "outage": "availability",
    "sabotage": "availability",
    "copyright": "fraud",
    "masquerade": "fraud",
    "phishing": "fraud",
    "unauthorized-use-of-resources": "fraud",
    "Unauthorised-information-access": "information content security",
    "Unauthorised-information-modification": "information content security",
    "data-loss": "information content security",
    "dropzone": "information content security",  # not in ENISA eCSIRT-II taxonomy
    "leak": "information content security",  # not in ENISA eCSIRT-II taxonomy
    "scanner": "information-gathering",
    "sniffing": "information-gathering",
    "social-engineering": "information-gathering",
    "brute-force": "intrusion attempts",
    "exploit": "intrusion attempts",
    "ids-alert": "intrusion attempts",
    "application-compromise": "intrusions",
    "backdoor": "intrusions",  # not in ENISA eCSIRT-II taxonomy
    "burglary": "intrusions",
    "compromised": "intrusions",  # not in ENISA eCSIRT-II taxonomy,
    "defacement": "intrusions",  # not in ENISA eCSIRT-II taxonomy
    "privileged-account-compromise": "intrusions",
    "unauthorized-command": "intrusions",  # not in ENISA eCSIRT-II taxonomy
    "unauthorized-login": "intrusions",  # not in ENISA eCSIRT-II taxonomy
    "unprivileged-account-compromise": "intrusions",
    "c2server": "malicious code",  # ENISA eCSIRT-II taxonomy: 'c2server'
    "dga domain": "malicious code",  # not in ENISA eCSIRT-II taxonomy
    "infected-system": "malicious code",  # ENISA eCSIRT-II taxonomy: 'infected-system'
    "malware": "malicious code",  # not in ENISA eCSIRT-II taxonomy
    "malware-configuration": "malicious code",  # ENISA eCSIRT-II taxonomy: 'malware-configuration'
    "malware-distribution": "malicious code",
    "ransomware": "malicious code",  # not in ENISA eCSIRT-II taxonomy
    "blacklist": "other",
    "other": "other",  # not in ENISA eCSIRT-II taxonomy
    "proxy": "other",  # not in ENISA eCSIRT-II taxonomy
    "tor": "other",  # not in ENISA eCSIRT-II taxonomy
    "unknown": "other",  # not in ENISA eCSIRT-II taxonomy
    "test": "test",
    "ddos-amplifier": "vulnerable",
    "information-disclosure": "vulnerable",
    "potentially-unwanted-accessible": "vulnerable",
    "vulnerable client": "vulnerable",  # not in ENISA eCSIRT-II taxonomy
    "vulnerable service": "vulnerable",  # not in ENISA eCSIRT-II taxonomy
    "vulnerable-system": "vulnerable",
    "weak-crypto": "vulnerable",
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
            # classification given, type given... don't change it
            pass

        self.send_message(event)
        self.acknowledge_message()


BOT = TaxonomyExpertBot
