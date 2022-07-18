# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def configuration(configuration, harmonization, dry_run, **kwargs):
    """
    Migrating configuration
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.misp.collector":
            if "misp_verify" not in bot["parameters"]:
                continue
            if bot["parameters"]["misp_verify"] != configuration['global']["http_verify_cert"]:
                bot["parameters"]["http_verify_cert"] = bot["parameters"]["misp_verify"]
            del bot["parameters"]["misp_verify"]
            changed = True
        elif bot["module"] == "intelmq.bots.outputs.elasticsearch.output":
            if "elastic_doctype" in bot["parameters"]:
                del bot["parameters"]["elastic_doctype"]
    return changed, configuration, harmonization


def azure_collector(configuration, harmonization, dry_run, **kwargs):
    """
    Checking for the Microsoft Azure collector
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.microsoft.collector_azure":
            if "connection_string" not in bot["parameters"]:
                changed = ("The Microsoft Azure collector changed backwards-"
                           "incompatible in IntelMQ 2.2.0. Look at the bot's "
                           "documentation and NEWS file to adapt the "
                           "configuration.")
    return changed, configuration, harmonization


def feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrates feed configuration for changed feed parameters.
    """
    found_urlvir_feed = []
    found_urlvir_parser = []
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.http.collector_http":
            if "http_url" not in bot["parameters"]:
                continue
            if bot["parameters"]["http_url"].startswith("http://www.urlvir.com/export-"):
                found_urlvir_feed.append(bot_id)
        elif bot['module'] == "intelmq.bots.parsers.urlvir.parser":
            found_urlvir_parser.append(bot_id)
    if found_urlvir_feed:
        messages.append('A discontinued feed "URLVir" has been found '
                        'as bot %s.' % ', '.join(sorted(found_urlvir_feed)))
    if found_urlvir_parser:
        messages.append('The removed parser "URLVir" has been found '
                        'as bot %s.' % ', '.join(sorted(found_urlvir_parser)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else None, configuration, harmonization
