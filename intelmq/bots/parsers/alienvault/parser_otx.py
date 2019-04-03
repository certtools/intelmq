# -*- coding: utf-8 -*-
"""
Events are gathered based on user subscriptions in AlienVault OTX
The data structure is described in detail here:
https://github.com/AlienVault-Labs/OTX-Python-SDK/blob/master/
howto_use_python_otx_api.ipynb
"""

import json
import urllib.parse as parse

from intelmq.lib.bot import ParserBot

HASHES = {
    'FileHash-SHA256': 'malware.hash.sha256',
    'FileHash-SHA1': 'malware.hash.sha1',
    'FileHash-MD5': 'malware.hash.md5'
}


class AlienVaultOTXParserBot(ParserBot):
    parse = ParserBot.parse_json
    recover_line = ParserBot.recover_line_json

    def parse_line(self, pulse, report):
        additional_pulse = {"author": pulse['author_name'],
                            "pulse": pulse['name']}

        events = []
        for indicator in pulse["indicators"]:
            additional_indicator = {}
            event = self.new_event(report)
            # hashes
            if indicator["type"] in HASHES.keys():
                event.add(HASHES[indicator["type"]], indicator["indicator"])
            # fqdn
            elif indicator["type"] in ['hostname', 'domain']:
                # not all domains in the report are just domains
                # some are URLs, we can manage those here instead
                # of raising errors
                #
                # dirty check if there is a scheme

                resource = indicator["indicator"] \
                    if '://' in indicator["indicator"] \
                    else 'http://' + indicator["indicator"]
                path = parse.urlparse(resource).path
                if len(path) > 0:
                    event.add('source.url', resource)
                # CIDR
                elif indicator["type"] in ['CIDR']:
                    event.add('source.network',
                              indicator["indicator"])

                # CVE
                elif indicator["type"] in ['CVE']:
                    additional_indicator['CVE'] = indicator["indicator"]
                    # TODO: Process these IoCs: FilePath, Mutex
                else:
                    event.add('source.fqdn', indicator["indicator"])
            # IP addresses
            elif indicator["type"] in ['IPv4', 'IPv6']:
                event.add('source.ip', indicator["indicator"])
            # emails
            elif indicator["type"] == 'email':
                event.add('source.account', indicator["indicator"])
            # URLs/URIs, OTX URIs can contain both full url or only path
            elif indicator["type"] in ['URL', 'URI']:
                resource = indicator["indicator"] \
                    if '://' in indicator["indicator"] \
                    else 'http://' + indicator["indicator"]
                uri_added = event.add('source.url', resource, raise_failure=False)
                if not uri_added:
                    if indicator["type"] == 'URI':
                        event.add('source.urlpath', indicator["indicator"])
                    else:
                        raise ValueError("Invalid value %r for URL hamonization type." % indicator["indicator"])
            # CIDR
            elif indicator["type"] in ['CIDR']:
                event.add('source.network', indicator["indicator"])

            # CVE
            elif indicator["type"] in ['CVE']:
                additional_indicator['CVE'] = indicator["indicator"]
                # TODO: Process these IoCs: FilePath, Mutex
            else:
                continue

            # if pulse_key exists in the indicators use it
            # else use id from pulse and add it as pulse_key
            # same logic is followed by alienvault
            if 'pulse_key' in indicator:
                additional_indicator['pulse_key'] = indicator['pulse_key']
            else:
                additional_indicator['pulse_key'] = pulse['id']
            if 'tags' in pulse:
                additional_indicator['tags'] = pulse['tags']
            if 'modified' in pulse:
                if '.' in pulse["modified"]:
                    additional_indicator['time_updated'] = \
                        pulse["modified"][:-4] + "+00:00"
                else:
                    additional_indicator['time_updated'] = \
                        pulse["modified"] + ".00+00:00"
            if 'industries' in pulse:
                additional_indicator['industries'] = pulse["industries"]
            if 'adversary' in pulse:
                additional_indicator['adversary'] = pulse["adversary"]
            if 'targeted_countries' in pulse:
                tc = pulse['targeted_countries']
                if tc:
                    additional_indicator['targeted_countries'] = tc
            if 'TLP' in pulse:
                event['tlp'] = pulse["TLP"]

            additional = additional_pulse.copy()
            additional.update(additional_indicator)

            event.add('comment', pulse['description'])
            event.add('extra', additional)
            event.add('classification.type', 'blacklist')
            event.add('time.source', indicator["created"][:-4] + "+00:00")
            event.add("raw", json.dumps(indicator, sort_keys=True))
            events.append(event)
        return events


BOT = AlienVaultOTXParserBot
