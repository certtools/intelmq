# -*- coding: utf-8 -*-
"""
Events are gathered based on user subscriptions in AlienVault OTX
The data structure is described in detail here:
https://github.com/AlienVault-Labs/OTX-Python-SDK/blob/master/
howto_use_python_otx_api.ipynb
"""

import json
import urllib.parse as parse

from intelmq.lib import utils
from intelmq.lib.bot import Bot

HASHES = {
    'FileHash-SHA256': '$5$',
    'FileHash-SHA1': '$sha1$',
    'FileHash-MD5': '$1$'
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
                    event.add('malware.hash', HASHES[indicator["type"]] +
                              indicator["indicator"])
                    additional['malware.hash.type'] = indicator["type"]
                    additional['malware.hash.raw'] = indicator["indicator"]
                # fqdn
                elif indicator["type"] in ['hostname', 'domain']:
                    # not all domains in the report are just domains
                    # some are urls, we can manage those here instead
                    # of raising errors
                    #
                    # dirty check if there is a scheme

                    resource = indicator["indicator"] \
                        if '://' in indicator["indicator"] \
                        else 'http://' + indicator["indicator"]
                    path = parse.urlparse(resource).path
                    if len(path) > 0:
                        event.add('source.url', resource)
                    else:
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
                    resource = indicator["indicator"] \
                        if '://' in indicator["indicator"] \
                        else 'http://' + indicator["indicator"]
                    event.add('source.url', resource)
                # CIDR
                elif indicator["type"] in ['CIDR']:
                    event.add('source.network',
                              indicator["indicator"])

                # CVE
                elif indicator["type"] in ['CVE']:
                    additional['CVE'] = indicator["indicator"]
                    # TODO: Process these IoCs: FilePath, Mutex
                else:
                    continue

                if 'tags' in pulse:
                    additional['tags'] = pulse['tags']
                if 'modified' in pulse:
                    additional['time_updated'] = \
                        pulse["modified"][:-4] + "+00:00"
                if 'industries' in pulse:
                    additional['industries'] = pulse["industries"]
                if '' in pulse:
                    additional['targeted_countries'] = \
                        pulse["targeted_countries"]
                if 'adversary' in pulse:
                    additional['adversary'] = pulse["adversary"]
                event.add('comment', pulse['description'])
                event.add('extra', additional)
                event.add('classification.type', 'blacklist')
                event.add('time.source', indicator["created"][:-4] + "+00:00")
                event.add("raw", json.dumps(indicator, sort_keys=True))
                self.send_message(event)
        self.acknowledge_message()


BOT = AlienVaultOTXParserBot
