# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def defaults_process_manager(configuration, harmonization, dry_run, **kwargs):
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
