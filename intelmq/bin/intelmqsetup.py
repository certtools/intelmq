# -*- coding: utf-8 -*-
"""
© 2019-2021 nic.at GmbH <intelmq-team@cert.at>

SPDX-License-Identifier: AGPL-3.0-only

Sets up an intelmq environment after installation or upgrade by
 * creating needed directories
 * set intelmq as owner for those
 * providing example configuration files if not already existing

Reasoning:
Pip does not (and cannot) create `/opt/intelmq`/user-given ROOT_DIR, as described in
https://github.com/certtools/intelmq/issues/819
"""
import argparse
import glob
import os
import shutil
import sys
import pkg_resources

from grp import getgrnam
from pwd import getpwuid, getpwnam
from typing import Optional

try:
    import intelmq_api
except ImportError:
    intelmq_api = None

from termstyle import red
from intelmq import (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                     VAR_STATE_PATH, BOTS_FILE, STATE_FILE_PATH)
from intelmq.bin.intelmqctl import IntelMQController


MANAGER_CONFIG_DIR = os.path.join(CONFIG_DIR, 'manager/')
FILE_OUTPUT_PATH = os.path.join(VAR_STATE_PATH, 'file-output/')


def basic_checks(skip_ownership):
    if os.geteuid() != 0 and not skip_ownership:
        sys.exit(red('You need to run this program as root for setting file ownership!'))
    if not ROOT_DIR:
        sys.exit(red('Not a pip-installation of IntelMQ, nothing to initialize.'))

    if skip_ownership:
        return
    try:
        getpwnam('intelmq')
    except KeyError:
        sys.exit(red("User 'intelmq' does not exist. Please create it and then re-run this program."))
    try:
        getgrnam('intelmq')
    except KeyError:
        sys.exit(red("Group 'intelmq' does not exist. Please create it and then re-run this program."))


def create_directory(directory: str, octal_mode: int, readable_mode: str):
    if not os.path.isdir(directory):
        os.makedirs(directory, mode=octal_mode,
                    exist_ok=True)
        print(f'Created directory {directory!r} with permissions {readable_mode}.')
    else:
        actual_mode = stat.filemode(os.stat(directory).st_mode)
        if actual_mode != readable_mode:
            print(f'Fixed wrong permissions of {directory!r}: {actual_mode!r} -> {readable_mode!r}.')
            os.chmod(directory, octal_mode)


def change_owner(file: str, owner=None, group=None):
    if owner and getpwuid(os.stat(file).st_uid).pw_name != owner:
        print(f'Fixing owner of directory {file!r}.')
        shutil.chown(file, user=owner)
    if group and getpwuid(os.stat(file).st_gid).pw_name != group:
        print(f'Fixing group of directory {file!r}.')
        shutil.chown(file, group=group)


def intelmqsetup_core(ownership=True, state_file=STATE_FILE_PATH):
    directories_modes = ((FILE_OUTPUT_PATH, 0o755, 'drwxr-xr-x'),
                         (VAR_RUN_PATH, 0o755, 'drwxr-xr-x'),
                         (DEFAULT_LOGGING_PATH, 0o755, 'drwxr-xr-x'),
                         (CONFIG_DIR, 0o775, 'drwxrwxr-x'),
                         )
    for directory, octal_mode, readable_mode in directories_modes:
        create_directory(directory, octal_mode, readable_mode)

    example_confs = glob.glob(pkg_resources.resource_filename('intelmq', 'etc/*.conf'))
    for example_conf in example_confs:
        fname = os.path.split(example_conf)[-1]
        if os.path.exists(os.path.join(CONFIG_DIR, fname)):
            print(f'Not overwriting existing {fname!r} with example.')
        else:
            shutil.copy(example_conf, CONFIG_DIR)
            print(f'Use example {fname!r}.')

    if os.path.islink(BOTS_FILE):
        print('Skip writing BOTS file as it is a link.')
    else:
        print('Writing BOTS file.')
        shutil.copy(pkg_resources.resource_filename('intelmq', 'bots/BOTS'),
                    BOTS_FILE)

    if ownership:
        print('Setting intelmq as owner for it\'s directories.')
        for obj in (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                    VAR_STATE_PATH, FILE_OUTPUT_PATH):
            change_owner(obj, owner='intelmq')

    print('Calling `intelmqctl upgrade-config to update/create state file')
    controller = IntelMQController(interactive=False, no_file_logging=True,
                                   drop_privileges=False)
    controller.upgrade_conf(state_file=state_file, no_backup=True)


def main():
    parser = argparse.ArgumentParser("Set's up directories and example "
                                     "configurations for IntelMQ.")
    parser.add_argument('--skip-ownership', action='store_true',
                        help='Skip setting file ownership')
    parser.add_argument('--state-file',
                        help='The state file location to use.',
                        default=STATE_FILE_PATH)
    args = parser.parse_args()

    basic_checks(skip_ownership=args.skip_ownership)
    intelmqsetup_core(ownership=not args.skip_ownership,
                      state_file=args.state_file)


if __name__ == '__main__':
    main()
