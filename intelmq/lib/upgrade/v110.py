# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def shadowserver_feednames(configuration, harmonization, dry_run, **kwargs):
    """
    Replace deprecated Shadowserver feednames
    """
    mapping = {
        "Botnet-Drone-Hadoop": "Drone",
        "DNS-open-resolvers": "DNS-Open-Resolvers",
        "Open-NetBIOS": "Open-NetBIOS-Nameservice",
        "Ssl-Freak-Scan": "SSL-FREAK-Vulnerable-Servers",
        "Ssl-Scan": "SSL-POODLE-Vulnerable-Servers",
    }
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.shadowserver.parser":
            if bot["parameters"]["feedname"] in mapping:
                changed = True
                bot["parameters"]["feedname"] = mapping[bot["parameters"]["feedname"]]

    return changed, configuration, harmonization


def deprecations(configuration, harmonization, dry_run, **kwargs):
    """
    Checking for deprecated runtime configurations (stomp collector, cymru parser, ripe expert, collector feed parameter)
    """
    mapping = {
        "intelmq.bots.collectors.n6.collector_stomp": "intelmq.bots.collectors.stomp.collector",
        "intelmq.bots.parsers.cymru_full_bogons.parser": "intelmq.bots.parsers.cymru.parser_full_bogons",
    }
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] in mapping:
            bot["module"] = mapping[bot["module"]]
            changed = True
        if bot["module"] == "intelmq.bots.experts.ripencc_abuse_contact.expert":
            bot["module"] = "intelmq.bots.experts.ripe.expert"
            changed = True
        if bot["module"] == "intelmq.bots.experts.ripe.expert":
            if bot["parameters"].get("query_ripe_stat"):
                if "query_ripe_stat_asn" not in bot["parameters"]:
                    bot["parameters"]["query_ripe_stat_asn"] = bot["parameters"]["query_ripe_stat"]
                if "query_ripe_stat_ip" not in bot["parameters"]:
                    bot["parameters"]["query_ripe_stat_ip"] = bot["parameters"]["query_ripe_stat"]
                del bot["parameters"]["query_ripe_stat"]
                changed = True
        if bot["group"] == 'Collector' and bot["parameters"].get("feed") and not bot["parameters"].get("name"):
            try:
                bot["parameters"]["name"] = bot["parameters"]["feed"]
                del bot["parameters"]["feed"]
            except KeyError:
                pass
            else:
                changed = True

    return changed, configuration, harmonization
