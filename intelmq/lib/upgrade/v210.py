# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-


def deprecations(configuration, harmonization, dry_run, **kwargs):
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
