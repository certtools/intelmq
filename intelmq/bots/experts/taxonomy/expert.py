# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
    "spam": "abusive-content",
    "harmful-speech": "abusive-content",
    "violence": "abusive-content",
    "ddos": "availability",
    "dos": "availability",
    "outage": "availability",
    "sabotage": "availability",
    "misconfiguration": "availability",
    "copyright": "fraud",
    "masquerade": "fraud",
    "phishing": "fraud",
    "unauthorized-use-of-resources": "fraud",
    "unauthorised-information-access": "information-content-security",
    "unauthorised-information-modification": "information-content-security",
    "data-loss": "information-content-security",
    "data-leak": "information-content-security",
    "scanner": "information-gathering",
    "sniffing": "information-gathering",
    "social-engineering": "information-gathering",
    "brute-force": "intrusion-attempts",
    "exploit": "intrusion-attempts",
    "ids-alert": "intrusion-attempts",
    "application-compromise": "intrusions",
    "burglary": "intrusions",
    "privileged-account-compromise": "intrusions",
    "system-compromise": "intrusions",
    "unprivileged-account-compromise": "intrusions",
    "c2-server": "malicious-code",
    "dga-domain": "other",  # intentionally not in RSIT, see #1409, #1613 and https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/pull/32
    "infected-system": "malicious-code",
    "malware-configuration": "malicious-code",
    "malware-distribution": "malicious-code",
    "blacklist": "other",  # intentionally not in RSIT
    "other": "other",
    "undetermined": "other",
    "malware": "other",  # intentionally not in RSIT
    "proxy": "other",  # intentionally not in RSIT
    "tor": "other",  # intentionally not in RSIT
    "test": "test",
    "ddos-amplifier": "vulnerable",
    "information-disclosure": "vulnerable",
    "potentially-unwanted-accessible": "vulnerable",
    "vulnerable-system": "vulnerable",
    "weak-crypto": "vulnerable",
}


class TaxonomyExpertBot(Bot):
    """Apply the eCSIRT Taxonomy to all events"""

    def process(self):
        event = self.receive_message()

        if "classification.taxonomy" not in event and "classification.type" in event:
            # set the taxonomy based on the mapping above
            event_type = event.get("classification.type")
            taxonomy = TAXONOMY.get(event_type, 'other')
            event.add("classification.taxonomy", taxonomy)
        elif "classification.taxonomy" not in event and "classification.type" not in event:
            event.add("classification.taxonomy", 'other')
            event.add("classification.type", 'undetermined')
        elif "classification.taxonomy" in event and "classification.type" not in event:
            event.add("classification.type", 'undetermined')
        else:
            # classification given, type given... don't change it
            pass

        self.send_message(event)
        self.acknowledge_message()


BOT = TaxonomyExpertBot
