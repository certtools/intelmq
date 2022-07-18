# SPDX-FileCopyrightText: 2022 Birger Schacht
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def deprecations(configuration, harmonization, dry_run, **kwargs):
    """
    Deprecate malwaredomains parser and collector
    """
    found_malwaredomainsparser = []
    found_malwaredomainscollector = []
    changed = None
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.malwaredomains.parser":
            found_malwaredomainsparser.append(bot_id)
        if bot["module"] == "intelmq.bots.collectors.http.collector":
            if "http_url" not in bot["parameters"]:
                continue
            if bot["parameters"]["http_url"] == 'http://mirror1.malwaredomains.com/files/domains.txt':
                found_malwaredomainscollector.append(bot_id)
    if found_malwaredomainsparser:
        messages.append('A discontinued bot "Malware Domains Parser" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malwaredomainsparser)))
    if found_malwaredomainscollector:
        messages.append('A discontinued bot "Malware Domains Collector" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malwaredomainscollector)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else changed, configuration, harmonization
