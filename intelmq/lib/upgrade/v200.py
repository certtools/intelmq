# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def defaults_statistics(configuration, harmonization, dry_run, **kwargs):
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


def defaults_broker(configuration, harmonization, dry_run, **kwargs):
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


def defaults_ssl_ca_certificate(configuration, harmonization, dry_run, **kwargs):
    """
    Add ssl_ca_certificate to defaults
    """
    if "ssl_ca_certificate" not in configuration['global']:
        configuration['global']["ssl_ca_certificate"] = None
        return True, configuration, harmonization
    else:
        return None, configuration, harmonization
