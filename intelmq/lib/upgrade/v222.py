# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrate Shadowserver feed name
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.shadowserver.parser":
            if bot["parameters"].get("feedname", None) == "Blacklisted-IP":
                bot["parameters"]["feedname"] = "Blocklist"
                changed = True
    return changed, configuration, harmonization
