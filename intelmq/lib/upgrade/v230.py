# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def csv_parser_parameter_fix(configuration, harmonization, dry_run, **kwargs):
    """
    Fix CSV parser parameter misspelling
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.generic.parser_csv":
            if "delimeter" in bot["parameters"] and "delimiter" in bot["parameters"]:
                del bot["parameters"]["delimeter"]
                changed = True
            elif "delimeter" in bot["parameters"]:
                bot["parameters"]["delimiter"] = bot["parameters"]["delimeter"]
                del bot["parameters"]["delimeter"]
                changed = True
    return changed, configuration, harmonization


def deprecations(configuration, harmonization, dry_run, **kwargs):
    """
    Deprecate malwaredomainlist parser
    """
    found_malwaredomainlistparser = []
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.malwaredomainlist.parser":
            found_malwaredomainlistparser.append(bot_id)
    if found_malwaredomainlistparser:
        messages.append('A discontinued bot "Malware Domain List Parser" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malwaredomainlistparser)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else None, configuration, harmonization


def feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrates feeds' configuration for changed/fixed parameter
    """
    found_malwaredomainlist = []
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.http.collector_http":
            if "http_url" not in bot["parameters"]:
                continue
            if bot["parameters"]["http_url"].startswith("http://www.malwaredomainlist.com/updatescsv.php"):
                found_malwaredomainlist.append(bot_id)
    if found_malwaredomainlist:
        messages.append('A discontinued feed "Malware Domain List" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malwaredomainlist)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else None, configuration, harmonization
