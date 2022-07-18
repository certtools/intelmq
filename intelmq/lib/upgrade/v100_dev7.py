# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
from intelmq.lib.utils import load_configuration, write_configuration


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


def modify_syntax(configuration, harmonization, dry_run, **kwargs):
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
