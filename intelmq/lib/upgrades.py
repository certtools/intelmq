"""
© 2020 Sebastian Wagner <wagner@cert.at>

SPDX-License-Identifier: AGPL-3.0-or-later
"""
from collections import OrderedDict
from pkg_resources import resource_filename
from pathlib import Path
from intelmq import CONFIG_DIR

from intelmq.lib.utils import load_configuration, write_configuration

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
           'v213_deprecations',
           'v213_feed_changes',
           'v220_configuration',
           'v220_azure_collector',
           'v220_feed_changes',
           'v221_feed_changes',
           'v222_feed_changes',
           'v230_csv_parser_parameter_fix',
           'v230_deprecations',
           'v230_feed_changes',
           'v233_feodotracker_browse',
           'v300_bots_file_removal',
           'v300_defaults_file_removal',
           'v300_pipeline_file_removal',
           'v301_deprecations',
           'v310_feed_changes',
           'v310_shadowserver_feednames',
           ]


def v200_defaults_statistics(configuration, harmonization, dry_run, **kwargs):
    """
    Inserting `statistics_*` parameters into defaults configuration file
    """
    values = {"statistics_database": 3,
              "statistics_host": "127.0.0.1",
              "statistics_password": configuration['global'].get('source_pipeline_password', None),
              "statistics_port": 6379
              }
    changed = None
    for key, value in values.items():
        if key not in configuration['global']:
            configuration['global'][key] = value
            changed = True
    return changed, configuration, harmonization


def v200_defaults_broker(configuration, harmonization, dry_run, **kwargs):
    """
    Inserting `*_pipeline_broker` and deleting broker into/from defaults configuration
    """
    changed = None
    values = {"destination_pipeline_broker": configuration['global'].get("broker", "redis"),
              "source_pipeline_broker": configuration['global'].get("broker", "redis"),
              }
    for key, value in values.items():
        if key not in configuration['global']:
            configuration['global'][key] = value
            changed = True
    if "broker" in configuration['global']:
        del configuration['global']["broker"]
        changed = True

    return changed, configuration, harmonization


def v112_feodo_tracker_ips(configuration, harmonization, dry_run, **kwargs):
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


def v112_feodo_tracker_domains(configuration, harmonization, dry_run, **kwargs):
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


def v110_shadowserver_feednames(configuration, harmonization, dry_run, **kwargs):
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


def v110_deprecations(configuration, harmonization, dry_run, **kwargs):
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


def v100_dev7_modify_syntax(configuration, harmonization, dry_run, **kwargs):
    """
    Migrate modify bot configuration format
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.experts.modify.expert":
            if "configuration_path" in bot["parameters"]:
                config = load_configuration(bot["parameters"]["configuration_path"])
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
                        write_configuration(bot["parameters"]["configuration_path"],
                                            new_config)
                    except PermissionError:
                        return ('Can\'t update %s\'s configuration: Permission denied.' % bot_id,
                                configuration, harmonization)

    return changed, configuration, harmonization


def v200_defaults_ssl_ca_certificate(configuration, harmonization, dry_run, **kwargs):
    """
    Add ssl_ca_certificate to defaults
    """
    if "ssl_ca_certificate" not in configuration['global']:
        configuration['global']["ssl_ca_certificate"] = None
        return True, configuration, harmonization
    else:
        return None, configuration, harmonization


def v111_defaults_process_manager(configuration, harmonization, dry_run, **kwargs):
    """
    Fix typo in proccess_manager parameter
    """
    changed = None
    if "proccess_manager" in configuration['global']:
        if "process_manager" in configuration['global']:
            del configuration['global']["proccess_manager"]
        elif "process_manager" not in configuration['global']:
            configuration['global']["process_manager"] = configuration['global']["proccess_manager"]
            del configuration['global']["proccess_manager"]
        changed = True
    else:
        if "process_manager" not in configuration['global']:
            configuration['global']["process_manager"] = "intelmq"
            changed = True

    return changed, configuration, harmonization


def v202_fixes(configuration, harmonization, dry_run, **kwargs):
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


def v210_deprecations(configuration, harmonization, dry_run, **kwargs):
    """
    Migrating configuration
    """
    changed = None
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
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
    return changed, configuration, harmonization


def v213_deprecations(configuration, harmonization, dry_run, **kwargs):
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


def v220_configuration(configuration, harmonization, dry_run, **kwargs):
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


def v220_azure_collector(configuration, harmonization, dry_run, **kwargs):
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


def harmonization(configuration, harmonization, dry_run, **kwargs):
    """
    Checks if all harmonization fields and types are correct
    """
    changed = None
    original = load_configuration(resource_filename('intelmq',
                                                    'etc/harmonization.conf'))
    for msg_type, msg in original.items():
        if msg_type not in harmonization:
            harmonization[msg_type] = msg
            changed = True
            continue
        for fieldname, field in msg.items():
            if fieldname not in harmonization[msg_type]:
                harmonization[msg_type][fieldname] = field
                changed = True
                continue
            if harmonization[msg_type][fieldname]['type'] != original[msg_type][fieldname]['type']:
                harmonization[msg_type][fieldname]['type'] = original[msg_type][fieldname]['type']
                changed = True
            installed_regex = harmonization[msg_type][fieldname].get('regex')
            original_regex = original[msg_type][fieldname].get('regex')
            if original_regex and original_regex != installed_regex:
                harmonization[msg_type][fieldname]['regex'] = original[msg_type][fieldname]['regex']
                changed = True
            installed_regex = harmonization[msg_type][fieldname].get('iregex')
            original_regex = original[msg_type][fieldname].get('iregex')
            if original_regex and original_regex != installed_regex:
                harmonization[msg_type][fieldname]['iregex'] = original[msg_type][fieldname]['iregex']
                changed = True
    return changed, configuration, harmonization


def v213_feed_changes(configuration, harmonization, dry_run, **kwargs):
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


def v220_feed_changes(configuration, harmonization, dry_run, **kwargs):
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


def v221_feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrates feeds' configuration for changed/fixed parameters. Deprecation of HP Hosts file feed & parser.
    """
    found_hphosts_collector = []
    found_hphosts_parser = []
    messages = []
    ULRHAUS_OLD = ['time.source', 'source.url', 'status', 'extra.urlhaus.threat_type', 'source.fqdn', 'source.ip',
                   'source.asn', 'source.geolocation.cc']
    URLHAUS_NEW = ['time.source', 'source.url', 'status', 'classification.type|__IGNORE__', 'source.fqdn|__IGNORE__',
                   'source.ip', 'source.asn', 'source.geolocation.cc']
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


def v222_feed_changes(configuration, harmonization, dry_run, **kwargs):
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


def v230_csv_parser_parameter_fix(configuration, harmonization, dry_run, **kwargs):
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


def v230_deprecations(configuration, harmonization, dry_run, **kwargs):
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


def v230_feed_changes(configuration, harmonization, dry_run, **kwargs):
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


def v300_bots_file_removal(configuration, harmonization, dry_run, **kwargs):
    """
    Remove BOTS file
    """
    changed = None
    messages = []
    bots_file = Path(CONFIG_DIR) / "BOTS"
    if bots_file.exists():
        if dry_run:
            print(f'Would now remove file {bots_file!r}.')
        else:
            bots_file.unlink()
            changed = True
    messages = ' '.join(messages)
    return messages if messages else changed, configuration, harmonization


def v300_defaults_file_removal(configuration, harmonization, dry_run, **kwargs):
    """
    Remove the defaults.conf file
    """
    changed = None
    messages = []
    defaults_file = Path(CONFIG_DIR) / "defaults.conf"
    if defaults_file.exists():
        if dry_run:
            print(f'Would now remove file {defaults_file!r}.')
        else:
            configuration['global'] = load_configuration(defaults_file)
            defaults_file.unlink()
            changed = True
    messages = ' '.join(messages)
    return messages if messages else changed, configuration, harmonization


def v233_feodotracker_browse(configuration, harmonization, dry_run, **kwargs):
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
                (bot["parameters"]["columns"] == old_feodo_columns or bot["parameters"][
                    "columns"] == old_feodo_columns.split(',')) and
                (bot["parameters"]["ignore_values"] == old_ignore_values or bot["parameters"][
                    "ignore_values"] == old_ignore_values.split(','))):
            bot["parameters"][
                "columns"] = 'time.source,source.ip,malware.name,status,source.as_name,source.geolocation.cc'
            bot["parameters"]['ignore_values'] = ',,,,,'
            changed = True
    return changed, configuration, harmonization


def v300_pipeline_file_removal(configuration, harmonization, dry_run, **kwargs):
    """
    Remove the pipeline.conf file
    """
    changed = None
    messages = []
    pipeline_file = Path(CONFIG_DIR) / "pipeline.conf"
    if pipeline_file.exists():
        pipelines = load_configuration(pipeline_file)
        for bot in configuration:
            if bot == 'global':
                continue
            if bot in pipelines:
                if 'destination-queues' in pipelines[bot]:
                    destination_queues = pipelines[bot]['destination-queues']
                    if isinstance(destination_queues, dict):
                        configuration[bot]['parameters']['destination_queues'] = destination_queues
                    if isinstance(destination_queues, list):
                        configuration[bot]['parameters']['destination_queues'] = {'_default': destination_queues}
                    if isinstance(destination_queues, str):
                        configuration[bot]['parameters']['destination_queues'] = {'_default': [destination_queues]}
                if 'source-queue' in pipelines[bot]:
                    if pipelines[bot]['source-queue'] != f"{bot}-queue":
                        configuration[bot]['parameters']['source_queue'] = pipelines[bot]['source-queue']
        if dry_run:
            print(f'Would now remove file {pipeline_file!r}.')
        else:
            pipeline_file.unlink()
        changed = True
    messages = ' '.join(messages)
    return messages if messages else changed, configuration, harmonization


def v301_deprecations(configuration, harmonization, dry_run, **kwargs):
    """
    Deprecate malwaredomains parser and collector
    """
    found_malwaredomainsparser = []
    found_malwaredomainscollector = []
    changed = None
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.malwaredomains.parser":
            found_malwaredomainsparser.append(bot_id)
        if bot["module"] == "intelmq.bots.collectors.http.collector":
            if "http_url" not in bot["parameters"]:
                continue
            if bot["parameters"]["http_url"] == 'http://mirror1.malwaredomains.com/files/domains.txt':
                found_malwaredomainscollector.append(bot_id)
    if found_malwaredomainsparser:
        messages.append('A discontinued bot "Malware Domains Parser" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malwaredomainsparser)))
    if found_malwaredomainscollector:
        messages.append('A discontinued bot "Malware Domains Collector" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malwaredomainscollector)))
    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else changed, configuration, harmonization


def v310_shadowserver_feednames(configuration, harmonization, dry_run, **kwargs):
    """
    Remove legacy Shadowserver feednames
    """
    legacy = {
        'Amplification-DDoS-Victim': 1,
        'Blacklisted-IP': 1,
        'CAIDA-IP-Spoofer': 1,
        'Darknet': 1,
        'Drone': 1,
        'Drone-Brute-Force': 1,
        'HTTP-Scanners': 1,
        'ICS-Scanners': 1,
        'IPv6-Sinkhole-HTTP-Drone': 1,
        'Microsoft-Sinkhole': 1,
        'Outdated-DNSSEC-Key': 1,
        'Outdated-DNSSEC-Key-IPv6': 1,
        'Sinkhole-HTTP-Drone': 1
    }
    changed = None
    names = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.shadowserver.parser":
            if bot["parameters"]["feedname"] in legacy:
                names.append(bot["parameters"]["feedname"])
    return 'A discontinued feed has been found and must be removed %s' % ', '.join(names) if names else changed, configuration, harmonization


def v310_feed_changes(configuration, harmonization, dry_run, **kwargs):
    """
    Migrates feeds' configuration for changed/fixed parameter
    """
    found_autoshun = []
    found_malc0de = []
    found_dshield_domain = []
    found_abusech_removed_parsers = []
    found_abusech_feodotracker_csv = []
    found_abusech_feodotracker_browse = []
    found_viriback = []
    found_netlab_mirai_scanner = []
    found_benkow_panels = []
    found_taichung = []
    messages = []
    for bot_id, bot in configuration.items():
        if bot_id == 'global':
            continue
        if bot["module"] == "intelmq.bots.parsers.malc0de.parser":
            found_malc0de.append(bot_id)
        if bot["module"] == "intelmq.bots.collectors.http.collector":
            http_url = bot["parameters"].get("http_url", "")
            if http_url.startswith("https://malc0de.com/bl"):
                found_malc0de.append(bot_id)
            if http_url.startswith("https://www.autoshun.org/download"):
                found_autoshun.append(bot_id)
            if http_url.startswith("https://feodotracker.abuse.ch/browse"):
                found_abusech_feodotracker_browse.append(bot_id)
            if http_url.startswith("https://feodotracker.abuse.ch/downloads/ipblocklist.csv"):
                found_abusech_feodotracker_csv.append(bot_id)
            if http_url == "http://tracker.viriback.com/":
                found_viriback.append(bot_id)
            if http_url.startswith("http://data.netlab.360.com/feeds/mirai-scanner/scanner.list"):
                found_netlab_mirai_scanner.append(bot_id)
            if "benkow.cc/export.php" in http_url:  # both HTTP and HTTPS
                found_benkow_panels.append(bot_id)
            if http_url.startswith("https://www.tc.edu.tw/net/netflow/lkout/recent"):
                found_taichung.append(bot_id)
        if bot["module"] == "intelmq.bots.parsers.autoshun.parser":
            found_autoshun.append(bot_id)
        if bot["module"] == "intelmq.bots.parsers.dshield.parser_domain":
            found_dshield_domain.append(bot_id)
        if (bot["module"] == "intelmq.bots.parsers.abusech.parser_ip" or
                bot["module"] == "intelmq.bots.parsers.abusech.parser_domain"):
            found_abusech_removed_parsers.append(bot_id)
        if bot["module"] == "intelmq.bots.parsers.generic.parser_csv":
            if bot.get("parameters") and bot["parameters"].get("type"):
                bot["parameters"]["default_fields"] = {
                    "classification.type": bot["parameters"]["type"]
                }
                del bot["parameters"]["type"]
        if bot["module"] == "intelmq.bots.parsers.taichung.parser":
            found_taichung.append(bot_id)

    if found_malc0de:
        messages.append('A discontinued feed "Malc0de" has been found '
                        'as bot %s.' % ', '.join(sorted(found_malc0de)))
    if found_autoshun:
        messages.append('A discontinued feed "Autoshun" has been found '
                        'as bot %s.' % ', '.join(sorted(found_autoshun)))
    if found_dshield_domain:
        messages.append('A discontinued feed "DShield Suspicious Domain" has been found '
                        'as bot %s.' % ', '.join(sorted(found_dshield_domain)))

    if found_abusech_feodotracker_csv:
        messages.append('A discontinued feed "Abuse.ch Feodo Tracker IPs" has been found'
                        'as bot %s.\nPlease manually replace with the feed'
                        '"Abuse.ch Feodo Tracker".' % ', '.join(sorted(found_abusech_feodotracker_csv)))

    if found_abusech_feodotracker_browse:
        messages.append('A discontinued feed "Abuse.ch Feodo Tracker Browse" has been found'
                        'as bot %s.\nPlease manually replace with the feed'
                        '"Abuse.ch Feodo Tracker".' % ', '.join(sorted(found_abusech_feodotracker_browse)))

    if found_abusech_removed_parsers:
        messages.append('A discontinued bot module has been found'
                        'as bot %s.' % ', '.join(sorted(found_abusech_removed_parsers)))

    if found_viriback:
        messages.append('The feed "Viriback Unsafe Site" has been replaced. Please see the feed'
                        ' "Viriback C2 Tracker" and'
                        ' adjust your configuration. Affected bots: %s' % ', '.join(found_viriback))

    if found_netlab_mirai_scanner:
        messages.append('A discontinued feed "Netlab Mirai Scanner" has been found '
                        'as bot %s.' % ', '.join(sorted(found_netlab_mirai_scanner)))

    if found_benkow_panels:
        messages.append('The feed "Benkow Malware Panels Tracker" has been changed. Please see the feed\'s'
                        ' documentation and adjust your configuration.'
                        ' Affected bots: %s' % ', '.join(found_benkow_panels))

    if found_taichung:
        messages.append('A discontinued feed "Taichung" has been found '
                        'as bot %s.' % ', '.join(sorted(found_taichung)))

    messages = ' '.join(messages)
    return messages + ' Remove affected bots yourself.' if messages else None, configuration, harmonization


UPGRADES = OrderedDict([
    ((1, 0, 0, 'dev7'), (v100_dev7_modify_syntax,)),
    ((1, 1, 0), (v110_shadowserver_feednames, v110_deprecations)),
    ((1, 1, 1), (v111_defaults_process_manager,)),
    ((1, 1, 2), (v112_feodo_tracker_ips, v112_feodo_tracker_domains,)),
    ((2, 0, 0), (v200_defaults_statistics, v200_defaults_broker,
                 v200_defaults_ssl_ca_certificate)),
    ((2, 0, 1), ()),
    ((2, 0, 2), (v202_fixes,)),
    ((2, 1, 0), (v210_deprecations,)),
    ((2, 1, 1), ()),
    ((2, 1, 2), ()),
    ((2, 1, 3), (v213_deprecations, v213_feed_changes)),
    ((2, 2, 0), (v220_configuration, v220_azure_collector, v220_feed_changes)),
    ((2, 2, 1), (v221_feed_changes,)),
    ((2, 2, 2), (v222_feed_changes,)),
    ((2, 2, 3), ()),
    ((2, 3, 0), (v230_csv_parser_parameter_fix, v230_feed_changes, v230_deprecations,)),
    ((2, 3, 1), ()),
    ((2, 3, 2), ()),
    ((2, 3, 3), (v233_feodotracker_browse,)),
    ((3, 0, 0), (v300_bots_file_removal, v300_defaults_file_removal, v300_pipeline_file_removal,)),
    ((3, 0, 1), (v301_deprecations,)),
    ((3, 0, 2), ()),
    ((3, 1, 0), (v310_feed_changes, v310_shadowserver_feednames)),
    ((3, 2, 0), ()),
])

ALWAYS = (harmonization,)
