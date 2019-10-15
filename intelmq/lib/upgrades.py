# -*- coding: utf-8 -*-
"""
© 2019 Sebastian Wagner <wagner@cert.at>

SPDX-License-Identifier: AGPL-3.0
"""
from collections import OrderedDict

import intelmq.lib.utils as utils

__all__ = ['v100_dev7_modify_syntax',
           'v110_shadowserver_feednames',
           'v110_deprecations',
           'v200_defaults_statistics',
           'v200_defaults_broker',
           'v112_feodo_tracker_ips',
           'v112_feodo_tracker_domains',
           'v200_defaults_ssl_ca_certificate',
           'v111_defaults_process_manager',
           'v202_fixes',
           'v210_deprecations',
           ]


def v200_defaults_statistics(defaults, runtime, dry_run):
    """
    Inserting `statistics_*` parameters into defaults configuration file
    """
    values = {"statistics_database": 3,
              "statistics_host": "127.0.0.1",
              "statistics_password": defaults.get('source_pipeline_password', None),
              "statistics_port": 6379
              }
    changed = None
    for key, value in values.items():
        if key not in defaults:
            defaults[key] = value
            changed = True
    return changed, defaults, runtime


def v200_defaults_broker(defaults, runtime, dry_run):
    """
    Inserting `*_pipeline_broker` and deleting broker into/from defaults configuration
    """
    changed = None
    values = {"destination_pipeline_broker": defaults.get("broker", "redis"),
              "source_pipeline_broker": defaults.get("broker", "redis"),
              }
    for key, value in values.items():
        if key not in defaults:
            defaults[key] = value
            changed = True
    if "broker" in defaults:
        del defaults["broker"]
        changed = True

    return changed, defaults, runtime


def v112_feodo_tracker_ips(defaults, runtime, dry_run):
    """
    Fix URL of feodotracker IPs feed in runtime configuration
    """
    changed = None
    for bot_id, bot in runtime.items():
        if bot["parameters"].get("http_url") == "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist":
            bot["parameters"]["http_url"] = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
            changed = True

    return changed, defaults, runtime


def v112_feodo_tracker_domains(defaults, runtime, dry_run):
    """
    Search for discontinued feodotracker domains feed
    """
    found = False
    for bot_id, bot in runtime.items():
        if bot["parameters"].get("http_url") == "https://feodotracker.abuse.ch/blocklist/?download=domainblocklist":
            found = bot_id

    if not found:
        return None, defaults, runtime
    else:
        return ('The discontinued feed "Feodo Tracker Domains" has been found '
                'as bot %r. Remove it yourself please.' % found,
                defaults, runtime)


def v110_shadowserver_feednames(defaults, runtime, dry_run):
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
    for bot_id, bot in runtime.items():
        if bot["module"] == "intelmq.bots.parsers.shadowserver.parser":
            if bot["parameters"]["feedname"] in mapping:
                changed = True
                bot["parameters"]["feedname"] = mapping[bot["parameters"]["feedname"]]

    return changed, defaults, runtime


def v110_deprecations(defaults, runtime, dry_run):
    """
    Checking for deprecated runtime configurations (stomp collector, cymru parser, ripe expert)
    """
    mapping = {
        "intelmq.bots.collectors.n6.collector_stomp": "intelmq.bots.collectors.stomp.collector",
        "intelmq.bots.parsers.cymru_full_bogons.parser": "intelmq.bots.parsers.cymru.parser_full_bogons",
    }
    changed = None
    for bot_id, bot in runtime.items():
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

    return changed, defaults, runtime


def modify_expert_convert_config(old):
    """
    Also used in the modify expert
    """
    config = []
    for groupname, group in old.items():
        for rule_name, rule in group.items():
            config.append({"rulename": groupname + ' ' + rule_name,
                           "if": rule[0],
                           "then": rule[1]})
    return config


def v100_dev7_modify_syntax(defaults, runtime, dry_run):
    """
    Migrate modify bot configuration format
    """
    changed = None
    for bot_id, bot in runtime.items():
        if bot["module"] == "intelmq.bots.experts.modify.expert":
            if "configuration_path" in bot["parameters"]:
                config = utils.load_configuration(bot["parameters"]["configuration_path"])
                if type(config) is dict:
                    new_config = modify_expert_convert_config(config)
                    if len(config) != len(new_config):
                        return 'Error converting modify expert syntax. Different size of configurations. Please report this.'
                    changed = True
                    if dry_run:
                        print('Would now convert file %r syntax.',
                              bot["parameters"]["configuration_path"])
                        continue
                    try:
                        utils.write_configuration(bot["parameters"]["configuration_path"],
                                                  new_config)
                    except PermissionError:
                        return ('Can\'t update %s\'s configuration: Permission denied.' % bot_id,
                                defaults, runtime)

    return changed, defaults, runtime


def v200_defaults_ssl_ca_certificate(defaults, runtime, dry_run):
    """
    Add ssl_ca_certificate to defaults
    """
    if "ssl_ca_certificate" not in defaults:
        defaults["ssl_ca_certificate"] = None
        return True, defaults, runtime
    else:
        return None, defaults, runtime


def v111_defaults_process_manager(defaults, runtime, dry_run):
    """
    Fix typo in proccess_manager parameter
    """
    changed = None
    if "proccess_manager" in defaults:
        if "process_manager" in defaults:
            del defaults["proccess_manager"]
        elif "process_manager" not in defaults:
            defaults["process_manager"] = defaults["proccess_manager"]
            del defaults["proccess_manager"]
        changed = True
    else:
        if "process_manager" not in defaults:
            defaults["process_manager"] = "intelmq"
            changed = True

    return changed, defaults, runtime


def v202_fixes(defaults, runtime, dry_run):
    """
    Migrating collector parameter `feed` to `name`. RIPE expert set: `query_ripe_stat_ip` with `query_ripe_stat_asn` as default
    """
    changed = None
    for bot_id, bot in runtime.items():
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

    return changed, defaults, runtime


def v210_deprecations(defaults, runtime, dry_run):
    """
    Migrating configuration.
    """
    changed = None
    for bot_id, bot in runtime.items():
        if bot["module"] == "intelmq.bots.collectors.rt.collector_rt":
            # from 29c4b2c42b126ef51ac7287edc1a9fee28ab27fd to ce96e6d995d420e117a49a22d3bfdea762d899ec
            if "extract_files" in bot["parameters"]:
                bot["parameters"]["extract_attachment"] = bot["parameters"]["extract_files"]
                del bot["parameters"]["extract_files"]
                changed = True
            if "unzip_attachment" not in bot["parameters"]:
                continue
            if "extract_files" not in bot["parameters"]:
                bot["parameters"]["extract_attachment"] = bot["parameters"]["unzip_attachment"]
            del bot["parameters"]["unzip_attachment"]
            changed = True
        if bot["module"] in ("intelmq.bots.experts.generic_db_lookup.expert",
                             "intelmq.bots.outputs.postgresql.output"):
            if "engine" not in bot["parameters"]:
                bot["parameters"]["engine"] = "postgresql"
                changed = True
            if bot["module"] == "intelmq.bots.outputs.postgresql.output":
                bot["module"] = "intelmq.bots.outputs.sql.output"
                changed = True
    return changed, defaults, runtime


UPGRADES = OrderedDict([
    ((1, 0, 0, 'dev7'), (v100_dev7_modify_syntax, )),
    ((1, 1, 0), (v110_shadowserver_feednames, v110_deprecations)),
    ((1, 1, 1), (v111_defaults_process_manager, )),
    ((1, 1, 2), (v112_feodo_tracker_ips, v112_feodo_tracker_domains, )),
    ((2, 0, 0), (v200_defaults_statistics, v200_defaults_broker,
                 v200_defaults_ssl_ca_certificate)),
    ((2, 0, 1), ()),
    ((2, 0, 2), (v202_fixes, )),
    ((2, 1, 0), (v210_deprecations, )),
])
