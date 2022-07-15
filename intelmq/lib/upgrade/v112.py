# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def feodo_tracker_ips(configuration, harmonization, dry_run, **kwargs):
    """
    Fix URL of feodotracker IPs feed in runtime configuration
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["parameters"].get("http_url") == "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist":
            bot["parameters"]["http_url"] = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
            changed = True

    return changed, configuration, harmonization


def feodo_tracker_domains(configuration, harmonization, dry_run, **kwargs):
    """
    Search for discontinued feodotracker domains feed
    """
    found = False
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["parameters"].get("http_url") == "https://feodotracker.abuse.ch/blocklist/?download=domainblocklist":
            found = bot_id

    if not found:
        return None, configuration, harmonization
    else:
        return ('The discontinued feed "Feodo Tracker Domains" has been found '
                'as bot %r. Remove it yourself please.' % found,
                configuration, harmonization)
