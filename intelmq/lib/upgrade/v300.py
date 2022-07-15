# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
from pathlib import Path
from intelmq import CONFIG_DIR
from intelmq.lib.utils import load_configuration


def bots_file_removal(configuration, harmonization, dry_run, **kwargs):
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


def defaults_file_removal(configuration, harmonization, dry_run, **kwargs):
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


def pipeline_file_removal(configuration, harmonization, dry_run, **kwargs):
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
