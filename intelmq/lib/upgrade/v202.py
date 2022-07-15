# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def fixes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrate Collector parameter `feed` to `name`. RIPE expert set `query_ripe_stat_ip` with `query_ripe_stat_asn` as default.
    Set cymru whois expert `overwrite` to true.
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["group"] == 'Collector' and bot["parameters"].get("feed"):
            try:
                bot["parameters"]["name"] = bot["parameters"]["feed"]
                del bot["parameters"]["feed"]
            except KeyError:
                pass
            else:
                changed = True
        if bot["module"] == "intelmq.bots.experts.ripe.expert":
            if "query_ripe_stat_asn" in bot["parameters"]:
                if "query_ripe_stat_ip" not in bot["parameters"]:
                    bot["parameters"]["query_ripe_stat_ip"] = bot["parameters"]["query_ripe_stat_asn"]
                    changed = True
        if bot["module"] in ("intelmq.bots.experts.cymru_whois.expert",
                             "intelmq.bots.experts.reverse_dns.expert",
                             "intelmq.bots.experts.modify.expert"):
            if "overwrite" not in bot["parameters"]:
                bot["parameters"]["overwrite"] = True
                changed = True

    return changed, configuration, harmonization
