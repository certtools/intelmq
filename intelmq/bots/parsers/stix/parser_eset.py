# SPDX-FileCopyrightText: 2025 Ladislav Baco
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Parser bot for ESET Threat Intelligence feeds
This bot parses STIX Indicators objects received from TAXII collector
Then it analyzes event's comments based on STIX indicator's description
and it adds classification.type and malware family info
It is recommended to apply TaxonomyExpertBot then to map the taxonomy
"""

import re

from intelmq.bots.parsers.stix.parser import StixParserBot


CLASSIFICATION_BY_STRING = {
    'Host actively distributes high-severity malicious content in the form of executable code.': 'malware-distribution',
    'Host actively distributes high-severity threat in the form of executable code.': 'malware-distribution',
    'Host actively distributes high-severity threat in the form of malicious code.': 'malware-distribution',
    'Host actively distributes high-severity threat in the form of script code.': 'malware-distribution',
    'Host is known to be actively distributing adware or other medium-risk software.': 'malware-distribution',
    'Host is known to be actively distributing high-severity mobile threats or low-risk software.': 'other',
    'Host is known to be actively distributing threats or is of uncertain reputation.': 'other',
    'Host is known to be distributing low-risk and potentially unwanted content.': 'other',
    'Host actively distributes potentially unwanted or unsafe threat.': 'other',
    'Host is known source of phishing or other fraudulent content.': 'phishing',
    'Host is known source of active fraudulent content.': 'other',
    'Host is used as command and control server.': 'c2-server',
    'Web services scanning and attacks': 'scanner',
    'RDP bruteforce IP': 'brute-force',
    'SQL bruteforce IP': 'brute-force',
    'SMB bruteforce IP': 'brute-force',
    'MySQL bruteforce IP': 'brute-force',
    'FTP bruteforce IP': 'brute-force'
}

CLASSIFICATION_REGEX = {
    'C&C indicates that a botnet ([^ ]+) ([^ ]+) is present.': 'c2-server',
    'C&C of ([^ ]+) ([^ ]+)': 'c2-server',
    'Host is used as command and control server of ([^ ]+) ([^ ]+) malware family.': 'c2-server',
    'Each of these file hashes indicates that a variant of ([^ ]+) ([^ ]+) is present.': 'malware',
    '^[.* ]?([^ ]+) C&C server.*$': 'c2-server',
    '^[.* ]?([^ ]+) backdoor.*$': 'malware',
    '^[.* ]?([^ ]+) trojan.*$': 'malware',
    '^[.* ]?([^ ]+) implant.*$': 'malware',
    'Loader for ([^ ]+).*$': 'malware'
}

CLASSIFICATION_BY_REGEX = {}
for (regex, classification_type) in CLASSIFICATION_REGEX.items():
    CLASSIFICATION_BY_REGEX[re.compile(regex)] = classification_type


class ESETStixParserBot(StixParserBot):
    """Add classification.type and malware family to events"""

    # Platform/Type.Family.Variant!Suffixes
    # Type and suffixes are optional
    _malware_naming_convention_pattern = re.compile(r'^([^/]*/)?([^\.]*\.)?([^\.]+)(\.[^!]*)(!.*)?$')

    def parse_vendor_specific(self, event, line, report):
        classification_type = event.get('classification.type', 'undetermined')
        if classification_type == 'undetermined':
            comment = event.get('comment', '')
            classification_type, malware_name = self.classify(comment)
            event.add('classification.type', classification_type, overwrite=True)
            if malware_name:
                event.add('malware.name', malware_name)
        else:
            # classification.type already present, do not change it
            pass

    @staticmethod
    def classify(comment):
        """ Classify comment and returns (classification_type, malware_name) """
        classification_type = CLASSIFICATION_BY_STRING.get(comment, None)
        if classification_type:
            malware_name = None
            return (classification_type, malware_name)

        for (pattern, classification_type) in CLASSIFICATION_BY_REGEX.items():
            match = pattern.match(comment)
            if match:
                malware_name = None
                groups = match.groups()
                if len(groups) > 0:
                    malware = groups[0]
                    malware_name = ESETStixParserBot.extract_malware_family(malware)
                return (classification_type, malware_name)

        return ('undetermined', None)

    @staticmethod
    def extract_malware_family(malware):
        """ Extract malware family from the threat detection string """

        match = ESETStixParserBot._malware_naming_convention_pattern.match(malware)
        if match and len(match.groups()) == 5:
            malware_name = match.groups()[2]
        else:
            # usually just malware family (or unknown naming convention)
            malware_name = malware

        # IntelMQ malware.name should be lowercase
        return malware_name.lower()


BOT = ESETStixParserBot
