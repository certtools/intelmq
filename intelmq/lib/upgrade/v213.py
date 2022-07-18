# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def deprecations(configuration, harmonization, dry_run, **kwargs):
    """
    migrate attach_unzip to extract_files for mail attachment collector

    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.mail.collector_mail_attach":
            if "attach_unzip" not in bot["parameters"]:
                continue
            if "extract_files" in bot["parameters"] and "attach_unzip" in bot["parameters"]:
                del bot["parameters"]["attach_unzip"]
                changed = True
            elif "extract_files" not in bot["parameters"] and "attach_unzip" in bot["parameters"]:
                bot["parameters"]["extract_files"] = bot["parameters"]["attach_unzip"]
                del bot["parameters"]["attach_unzip"]
                changed = True
    return changed, configuration, harmonization


def feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrates feed configuration for changed feed parameters.
    """
    found_zeus = []
    found_bitcash = []
    found_ddos_attack = []
    found_ransomware = []
    found_bambenek = []
    found_nothink = []
    found_nothink_parser = []
    changed = None
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.collectors.http.collector_http":
            if "http_url" not in bot["parameters"]:
                continue
            if bot["parameters"]["http_url"] == 'https://www.tc.edu.tw/net/netflow/lkout/recent/30':
                bot["parameters"]["http_url"] = "https://www.tc.edu.tw/net/netflow/lkout/recent/"
                changed = True
            if bot["parameters"]["http_url"].startswith("https://zeustracker.abuse.ch/"):
                found_zeus.append(bot_id)
            elif bot["parameters"]["http_url"].startswith("https://bitcash.cz/misc/log/blacklist"):
                found_bitcash.append(bot_id)
            elif bot["parameters"]["http_url"].startswith("https://ransomwaretracker.abuse.ch/feeds/csv/"):
                found_ransomware.append(bot_id)
            elif bot["parameters"]["http_url"] == "https://osint.bambenekconsulting.com/feeds/dga-feed.txt":
                bot["parameters"]["http_url"] = "https://faf.bambenekconsulting.com/feeds/dga-feed.txt"
                changed = True
            elif bot["parameters"]["http_url"] in ("http://osing.bambenekconsulting.com/feeds/dga/c2-ipmasterlist.txt",
                                                   "https://osing.bambenekconsulting.com/feeds/dga/c2-ipmasterlist.txt",
                                                   "http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt",
                                                   "https://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt"):
                found_bambenek.append(bot_id)
            elif (bot["parameters"]["http_url"].startswith("http://www.nothink.org/") or
                  bot["parameters"]["http_url"].startswith("https://www.nothink.org/")):
                found_nothink.append(bot_id)
        elif bot["module"] == "intelmq.bots.collectors.http.collector_http_stream":
            if bot["parameters"].get("http_url", "").startswith("https://feed.caad.fkie.fraunhofer.de/ddosattackfeed"):
                found_ddos_attack.append(bot_id)
        elif bot['module'] == "intelmq.bots.parsers.nothink.parser":
            found_nothink_parser.append(bot_id)
    if found_zeus:
        messages.append('A discontinued feed "Zeus Tracker" has been found '
                        'as bot %s.' % ', '.join(sorted(found_zeus)))
    if found_bitcash:
        messages.append('The discontinued feed "Bitcash.cz" has been found '
                        'as bot %s.' % ', '.join(sorted(found_bitcash)))
    if found_ddos_attack:
        messages.append('The discontinued feed "Fraunhofer DDos Attack" has been found '
                        'as bot %s.' % ', '.join(sorted(found_ddos_attack)))
    if found_ransomware:
        messages.append('The discontinued feed "Abuse.ch Ransomware Tracker" has been found '
                        'as bot %s.' % ', '.join(sorted(found_ransomware)))
    if found_bambenek:
        messages.append('Many Bambenek feeds now require a license, see https://osint.bambenekconsulting.com/feeds/'
                        ' potentially affected bots are %s.' % ', '.join(sorted(found_bambenek)))
    if found_nothink:
        messages.append('All Nothink Honeypot feeds are discontinued, '
                        'potentially affected bots are %s.' % ', '.join(sorted(found_nothink)))
    if found_nothink_parser:
        messages.append('The Nothink Parser has been removed, '
                        'affected bots are %s.' % ', '.join(sorted(found_nothink_parser)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else changed, configuration, harmonization
