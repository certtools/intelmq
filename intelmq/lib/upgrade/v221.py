# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrates feeds' configuration for changed/fixed parameters. Deprecation of HP Hosts file feed & parser.
    """
    found_hphosts_collector = []
    found_hphosts_parser = []
    messages = []
    ULRHAUS_OLD = ['time.source', 'source.url', 'status', 'extra.urlhaus.threat_type', 'source.fqdn', 'source.ip', 'source.asn', 'source.geolocation.cc']
    URLHAUS_NEW = ['time.source', 'source.url', 'status', 'classification.type|__IGNORE__', 'source.fqdn|__IGNORE__', 'source.ip', 'source.asn', 'source.geolocation.cc']
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.http.collector_http":
            if bot["parameters"].get("http_url", None) == "http://hosts-file.net/download/hosts.txt":
                found_hphosts_collector.append(bot_id)
        elif bot['module'] == "intelmq.bots.parsers.hphosts.parser":
            found_hphosts_parser.append(bot_id)
        if bot["module"] == "intelmq.bots.parsers.generic.parser_csv":
            if "columns" not in bot["parameters"]:
                continue
            columns = bot["parameters"]["columns"]
            # convert columns to an array
            if type(columns) is str:
                columns = [column.strip() for column in columns.split(",")]
            if columns == ULRHAUS_OLD:
                changed = True
                bot["parameters"]["columns"] = URLHAUS_NEW

    if found_hphosts_collector:
        messages.append('A discontinued feed "HP Hosts File" has been found '
                        'as bot %s.' % ', '.join(sorted(found_hphosts_collector)))
    if found_hphosts_parser:
        messages.append('The removed parser "HP Hosts" has been found '
                        'as bot %s.' % ', '.join(sorted(found_hphosts_parser)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else changed, configuration, harmonization
