# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
from pkg_resources import resource_filename
from intelmq.lib.utils import load_configuration


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
