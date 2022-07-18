# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def feodotracker_browse(configuration, harmonization, dry_run, **kwargs):
    """
    Migrate Abuse.ch Feodotracker Browser feed parsing parameters
    """
    changed = None
    old_feodo_columns = 'time.source,source.ip,malware.name,status,extra.SBL,source.as_name,source.geolocation.cc'
    old_ignore_values = ',,,,Not listed,,'
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        # The parameters can be given as string or list of strings
        if (bot["module"] == "intelmq.bots.parsers.html_table.parser" and 'feodo' in bot_id.lower() and
                "columns" in bot["parameters"] and "ignore_values" in bot["parameters"] and
                (bot["parameters"]["columns"] == old_feodo_columns or bot["parameters"]["columns"] == old_feodo_columns.split(',')) and
                (bot["parameters"]["ignore_values"] == old_ignore_values or bot["parameters"]["ignore_values"] == old_ignore_values.split(','))):
            bot["parameters"]["columns"] = 'time.source,source.ip,malware.name,status,source.as_name,source.geolocation.cc'
            bot["parameters"]['ignore_values'] = ',,,,,'
            changed = True
    return changed, configuration, harmonization
