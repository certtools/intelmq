# -*- coding: utf-8 -*-
"""
Events are gathered based on user subscriptions in AlienVault OTX
The data structure is described in detail here:
https://github.com/AlienVault-Labs/OTX-Python-SDK/blob/master/
howto_use_python_otx_api.ipynb
"""

import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot

HASHES = {
    'FileHash-SHA256': 'malware.hash.sha256',
    'FileHash-SHA1': 'malware.hash.sha1',
    'FileHash-MD5': 'malware.hash.md5'
}


class AlienVaultOTXParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for pulse in json.loads(raw_report):
            additional = {"author": pulse['author_name'], "pulse": pulse['name']}
            for indicator in pulse["indicators"]:
                event = self.new_event(report)
                # hashes
                if indicator["type"] in HASHES.keys():
                    event.add(HASHES[indicator["type"]], indicator["indicator"])
                # fqdn
                if indicator["type"] in ['hostname', 'domain']:
                    event.add('source.fqdn',
                              indicator["indicator"])
                # IP addresses
                elif indicator["type"] in ['IPv4', 'IPv6']:
                    event.add('source.ip',
                              indicator["indicator"])
                # emails
                elif indicator["type"] == 'email':
                    event.add('source.account',
                              indicator["indicator"])
                # URLs
                elif indicator["type"] in ['URL', 'URI']:
                    event.add('source.url',
                              indicator["indicator"])
                # CIDR
                elif indicator["type"] in ['CIDR']:
                    event.add('source.network',
                              indicator["indicator"])
                # FilePath, Mutex, CVE - TODO: process these IoCs as well
                else:
                    continue

                event.add('comment', pulse['description'])
                event.add('extra', additional)
                event.add('classification.type', 'blacklist')
                event.add('time.source', indicator["created"][:-4] + "+00:00")
                event.add("raw", json.dumps(indicator, sort_keys=True))
                self.send_message(event)
        self.acknowledge_message()


BOT = AlienVaultOTXParserBot
